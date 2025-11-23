import googlemaps
from app.config import settings
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

class GoogleMapsService:
    """Service for Google Maps API integration"""
    
    def __init__(self):
        self.client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """Convert address to latitude/longitude"""
        try:
            result = self.client.geocode(address)
            if result:
                location = result[0]['geometry']['location']
                return (location['lat'], location['lng'])
            return None
        except Exception as e:
            print(f"Geocoding error: {e}")
            return None
    
    def reverse_geocode(self, lat: float, lng: float) -> Optional[str]:
        """Convert latitude/longitude to address"""
        try:
            result = self.client.reverse_geocode((lat, lng))
            if result:
                return result[0]['formatted_address']
            return None
        except Exception as e:
            print(f"Reverse geocoding error: {e}")
            return None
    
    def calculate_distance(
        self, 
        origin: Tuple[float, float], 
        destination: Tuple[float, float]
    ) -> Optional[Dict[str, Any]]:
        """Calculate distance and duration between two points"""
        try:
            result = self.client.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode="driving",
                departure_time=datetime.now()
            )
            
            if result['rows'][0]['elements'][0]['status'] == 'OK':
                element = result['rows'][0]['elements'][0]
                return {
                    'distance_km': element['distance']['value'] / 1000,
                    'duration_minutes': element['duration']['value'] / 60,
                    'distance_text': element['distance']['text'],
                    'duration_text': element['duration']['text']
                }
            return None
        except Exception as e:
            print(f"Distance calculation error: {e}")
            return None
    
    def find_nearby_places(
        self,
        lat: float,
        lng: float,
        place_type: str = "restaurant",
        radius: int = 5000
    ) -> List[Dict[str, Any]]:
        """Find nearby places of interest"""
        try:
            result = self.client.places_nearby(
                location=(lat, lng),
                radius=radius,
                type=place_type
            )
            
            places = []
            for place in result.get('results', []):
                places.append({
                    'name': place.get('name'),
                    'address': place.get('vicinity'),
                    'rating': place.get('rating'),
                    'lat': place['geometry']['location']['lat'],
                    'lng': place['geometry']['location']['lng'],
                    'types': place.get('types', [])
                })
            
            return places
        except Exception as e:
            print(f"Nearby places search error: {e}")
            return []
    
    def get_traffic_conditions(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float]
    ) -> Optional[Dict[str, Any]]:
        """Get current traffic conditions"""
        try:
            result = self.client.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode="driving",
                departure_time=datetime.now(),
                traffic_model="best_guess"
            )
            
            if result['rows'][0]['elements'][0]['status'] == 'OK':
                element = result['rows'][0]['elements'][0]
                
                duration = element['duration']['value']
                duration_in_traffic = element.get('duration_in_traffic', {}).get('value', duration)
                
                delay_minutes = (duration_in_traffic - duration) / 60
                
                return {
                    'normal_duration_minutes': duration / 60,
                    'current_duration_minutes': duration_in_traffic / 60,
                    'delay_minutes': delay_minutes,
                    'traffic_level': 'heavy' if delay_minutes > 15 else 'moderate' if delay_minutes > 5 else 'light'
                }
            return None
        except Exception as e:
            print(f"Traffic conditions error: {e}")
            return None
    
    def suggest_high_demand_zones(
        self,
        current_location: Tuple[float, float],
        city: str,
        time_of_day: str
    ) -> List[Dict[str, Any]]:
        """Suggest high-demand zones based on time and location"""
        # Popular zone types based on time of day
        zone_mapping = {
            'morning': ['transit_station', 'subway_station', 'school', 'hospital'],
            'afternoon': ['shopping_mall', 'restaurant', 'cafe'],
            'evening': ['restaurant', 'bar', 'movie_theater', 'shopping_mall'],
            'night': ['airport', 'hospital', 'night_club']
        }
        
        place_types = zone_mapping.get(time_of_day, ['restaurant'])
        
        suggestions = []
        for place_type in place_types:
            places = self.find_nearby_places(
                current_location[0],
                current_location[1],
                place_type=place_type,
                radius=10000  # 10km radius
            )
            
            for place in places[:3]:  # Top 3 per type
                distance_info = self.calculate_distance(
                    current_location,
                    (place['lat'], place['lng'])
                )
                
                if distance_info:
                    suggestions.append({
                        'zone_name': place['name'],
                        'latitude': place['lat'],
                        'longitude': place['lng'],
                        'distance_km': distance_info['distance_km'],
                        'travel_time_minutes': distance_info['duration_minutes'],
                        'zone_type': place_type,
                        'rating': place.get('rating', 0)
                    })
        
        # Sort by rating and distance
        suggestions.sort(key=lambda x: (x.get('rating', 0) * -1, x['distance_km']))
        
        return suggestions[:5]  # Return top 5


# Singleton instance
google_maps_service = GoogleMapsService()
