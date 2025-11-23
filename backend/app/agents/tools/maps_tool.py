from typing import Dict, Any, List, Tuple
from app.services.maps_service import google_maps_service
from datetime import datetime


class MapsTool:
    """Tool for Google Maps API operations"""
    
    def __init__(self):
        self.maps_service = google_maps_service
    
    def get_high_demand_zones(
        self,
        current_location: Tuple[float, float],
        city: str = "Bangalore"
    ) -> List[Dict[str, Any]]:
        """Get high-demand zones based on current time and location"""
        current_hour = datetime.now().hour
        
        # Determine time of day
        if 5 <= current_hour < 12:
            time_of_day = "morning"
        elif 12 <= current_hour < 17:
            time_of_day = "afternoon"
        elif 17 <= current_hour < 22:
            time_of_day = "evening"
        else:
            time_of_day = "night"
        
        zones = self.maps_service.suggest_high_demand_zones(
            current_location,
            city,
            time_of_day
        )
        
        # Add expected earnings based on zone type and time
        earnings_multiplier = {
            'morning': 1.2,
            'afternoon': 1.0,
            'evening': 1.5,
            'night': 1.3
        }
        
        for zone in zones:
            base_earnings = 150  # Base expected earnings
            zone['expected_earnings'] = base_earnings * earnings_multiplier[time_of_day]
            zone['confidence_score'] = min(zone.get('rating', 3) * 20, 100)
            zone['best_time'] = time_of_day
            
            # Add reason
            zone['reason'] = self._generate_zone_reason(zone, time_of_day)
        
        return zones
    
    def _generate_zone_reason(self, zone: Dict[str, Any], time_of_day: str) -> str:
        """Generate reason for zone recommendation"""
        zone_type = zone.get('zone_type', 'general')
        
        reasons = {
            'morning': {
                'transit_station': 'High demand for office commuters',
                'subway_station': 'Peak hour travel to work',
                'school': 'School drop-off time',
                'hospital': 'Early appointment traffic'
            },
            'afternoon': {
                'shopping_mall': 'Lunch crowd and shoppers',
                'restaurant': 'Lunch hour rush',
                'cafe': 'Afternoon meetings and breaks'
            },
            'evening': {
                'restaurant': 'Dinner rush hour',
                'shopping_mall': 'After-work shopping',
                'bar': 'Evening entertainment crowd',
                'movie_theater': 'Show time traffic'
            },
            'night': {
                'airport': '24/7 travel demand',
                'hospital': 'Emergency services',
                'night_club': 'Late night crowd'
            }
        }
        
        return reasons.get(time_of_day, {}).get(zone_type, 'High activity area')
    
    def calculate_trip_metrics(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float]
    ) -> Dict[str, Any]:
        """Calculate trip distance, duration, and traffic"""
        distance_info = self.maps_service.calculate_distance(origin, destination)
        traffic_info = self.maps_service.get_traffic_conditions(origin, destination)
        
        if not distance_info:
            return {}
        
        metrics = {
            'distance_km': distance_info['distance_km'],
            'estimated_duration_minutes': distance_info['duration_minutes'],
            'traffic_level': traffic_info.get('traffic_level', 'unknown') if traffic_info else 'unknown',
            'traffic_delay_minutes': traffic_info.get('delay_minutes', 0) if traffic_info else 0
        }
        
        # Estimate earnings based on distance
        base_rate = 10  # ₹10/km
        metrics['estimated_earnings'] = distance_info['distance_km'] * base_rate
        
        return metrics
    
    def geocode_location(self, address: str) -> Tuple[float, float]:
        """Convert address to coordinates"""
        coords = self.maps_service.geocode_address(address)
        return coords if coords else (0.0, 0.0)
    
    def reverse_geocode_location(self, lat: float, lng: float) -> str:
        """Convert coordinates to address"""
        address = self.maps_service.reverse_geocode(lat, lng)
        return address if address else "Unknown location"
