"""
Dynamic Earnings Database - Simulates real earnings tracking
No hardcoded values - generates realistic data based on patterns
"""
import json
import os
from datetime import datetime, timedelta
import random
from typing import Dict, List
from dataclasses import dataclass, asdict

@dataclass
class Trip:
    trip_id: str
    date: datetime
    source: str
    destination: str
    distance_km: float
    duration_minutes: int
    base_fare: float
    surge_multiplier: float
    total_fare: float
    tip: float
    platform: str  # uber, ola, zomato, swiggy
    weather_condition: str

class DynamicEarningsDB:
    def __init__(self, db_path: str = "earnings_data.json"):
        self.db_path = db_path
        self.trips: List[Trip] = []
        self.load_data()
    
    def load_data(self):
        """Load existing trip data or generate initial data"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                    for trip_data in data:
                        trip_data['date'] = datetime.fromisoformat(trip_data['date'])
                        self.trips.append(Trip(**trip_data))
            except:
                self._generate_sample_data()
        else:
            self._generate_sample_data()
    
    def save_data(self):
        """Save trip data to JSON file"""
        try:
            with open(self.db_path, 'w') as f:
                trips_data = []
                for trip in self.trips:
                    trip_dict = asdict(trip)
                    trip_dict['date'] = trip.date.isoformat()
                    trips_data.append(trip_dict)
                json.dump(trips_data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def _generate_sample_data(self):
        """Generate realistic sample trip data for the last 30 days"""
        platforms = ["Uber", "Ola", "Zomato", "Swiggy", "Direct"]
        weather_conditions = ["Clear", "Rainy", "Cloudy", "Foggy"]
        
        # Common Mumbai routes
        routes = [
            ("Bandra", "Andheri", 8, 25),
            ("Airport", "Bandra", 12, 35),
            ("Colaba", "Bandra", 15, 45),
            ("Powai", "BKC", 10, 30),
            ("Thane", "Andheri", 18, 50),
            ("Juhu", "Lower Parel", 14, 40),
            ("Worli", "Ghatkopar", 20, 55),
            ("Malad", "Churchgate", 25, 65)
        ]
        
        base_date = datetime.now() - timedelta(days=30)
        
        for day in range(30):
            current_date = base_date + timedelta(days=day)
            
            # Generate 3-15 trips per day based on weekday/weekend
            trips_per_day = random.randint(8, 15) if current_date.weekday() >= 5 else random.randint(3, 10)
            
            for trip_num in range(trips_per_day):
                # Select random route
                source, dest, base_distance, base_duration = random.choice(routes)
                
                # Add randomness to distance and duration
                distance = base_distance + random.uniform(-2, 3)
                duration = base_duration + random.randint(-10, 15)
                
                # Calculate fare based on distance and time of day
                hour = random.randint(6, 23)
                trip_time = current_date.replace(hour=hour, minute=random.randint(0, 59))
                
                # Surge pricing based on time and day
                surge = 1.0
                if hour in [7, 8, 9, 18, 19, 20]:  # Rush hours
                    surge = random.uniform(1.2, 2.0)
                elif hour >= 22 or hour <= 6:  # Night hours
                    surge = random.uniform(1.1, 1.5)
                elif current_date.weekday() >= 5:  # Weekend
                    surge = random.uniform(1.1, 1.6)
                
                # Weather impact
                weather = random.choice(weather_conditions)
                if weather == "Rainy":
                    surge *= random.uniform(1.2, 1.8)
                
                # Calculate base fare (₹10-15 per km + time component)
                base_fare = (distance * random.uniform(12, 18)) + (duration * 0.5)
                total_fare = base_fare * surge
                
                # Tips (20% chance of tip)
                tip = random.uniform(10, 50) if random.random() < 0.2 else 0
                
                # Platform selection
                platform = random.choice(platforms)
                
                trip = Trip(
                    trip_id=f"T{day:02d}{trip_num:02d}{random.randint(100,999)}",
                    date=trip_time,
                    source=source,
                    destination=dest,
                    distance_km=round(distance, 1),
                    duration_minutes=duration,
                    base_fare=round(base_fare, 2),
                    surge_multiplier=round(surge, 2),
                    total_fare=round(total_fare, 2),
                    tip=round(tip, 2),
                    platform=platform,
                    weather_condition=weather
                )
                
                self.trips.append(trip)
        
        self.save_data()
    
    def add_trip(self, source: str, destination: str, fare: float, platform: str = "Manual"):
        """Add a new trip to the database"""
        trip = Trip(
            trip_id=f"M{datetime.now().strftime('%Y%m%d%H%M%S')}",
            date=datetime.now(),
            source=source,
            destination=destination,
            distance_km=random.uniform(5, 20),
            duration_minutes=random.randint(15, 60),
            base_fare=fare,
            surge_multiplier=1.0,
            total_fare=fare,
            tip=0,
            platform=platform,
            weather_condition="Clear"
        )
        self.trips.append(trip)
        self.save_data()
    
    def get_earnings_by_period(self, period: str) -> Dict:
        """Get earnings data for specified period"""
        now = datetime.now()
        
        if period.lower() == "today":
            start_date = now.replace(hour=0, minute=0, second=0)
        elif period.lower() == "week":
            start_date = now - timedelta(days=7)
        elif period.lower() == "month":
            start_date = now - timedelta(days=30)
        else:
            start_date = now - timedelta(days=1)
        
        relevant_trips = [trip for trip in self.trips if trip.date >= start_date]
        
        if not relevant_trips:
            return {
                "total_earnings": 0,
                "total_trips": 0,
                "avg_per_trip": 0,
                "total_distance": 0,
                "total_tips": 0,
                "platform_breakdown": {},
                "period": period
            }
        
        total_earnings = sum(trip.total_fare for trip in relevant_trips)
        total_tips = sum(trip.tip for trip in relevant_trips)
        total_distance = sum(trip.distance_km for trip in relevant_trips)
        
        # Platform breakdown
        platform_earnings = {}
        for trip in relevant_trips:
            if trip.platform not in platform_earnings:
                platform_earnings[trip.platform] = {"earnings": 0, "trips": 0}
            platform_earnings[trip.platform]["earnings"] += trip.total_fare
            platform_earnings[trip.platform]["trips"] += 1
        
        return {
            "total_earnings": round(total_earnings, 2),
            "total_trips": len(relevant_trips),
            "avg_per_trip": round(total_earnings / len(relevant_trips), 2),
            "total_distance": round(total_distance, 1),
            "total_tips": round(total_tips, 2),
            "platform_breakdown": platform_earnings,
            "period": period
        }
    
    def get_route_analysis(self, source: str = None, destination: str = None) -> Dict:
        """Analyze earnings for specific routes"""
        if source:
            relevant_trips = [trip for trip in self.trips if source.lower() in trip.source.lower() or source.lower() in trip.destination.lower()]
        else:
            relevant_trips = self.trips
        
        if not relevant_trips:
            return {"message": "No trips found for specified route"}
        
        # Route statistics
        route_stats = {}
        for trip in relevant_trips:
            route_key = f"{trip.source} → {trip.destination}"
            if route_key not in route_stats:
                route_stats[route_key] = {
                    "trips": 0,
                    "total_earnings": 0,
                    "total_distance": 0,
                    "avg_surge": 0
                }
            
            stats = route_stats[route_key]
            stats["trips"] += 1
            stats["total_earnings"] += trip.total_fare
            stats["total_distance"] += trip.distance_km
            stats["avg_surge"] += trip.surge_multiplier
        
        # Calculate averages
        for route, stats in route_stats.items():
            if stats["trips"] > 0:
                stats["avg_earnings"] = round(stats["total_earnings"] / stats["trips"], 2)
                stats["avg_distance"] = round(stats["total_distance"] / stats["trips"], 1)
                stats["avg_surge"] = round(stats["avg_surge"] / stats["trips"], 2)
        
        # Sort by profitability
        sorted_routes = sorted(route_stats.items(), key=lambda x: x[1]["avg_earnings"], reverse=True)
        
        return {
            "route_analysis": dict(sorted_routes[:5]),  # Top 5 routes
            "total_routes_analyzed": len(route_stats)
        }

# Global instance
earnings_db = DynamicEarningsDB()