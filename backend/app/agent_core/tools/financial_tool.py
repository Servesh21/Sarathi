"""
Financial Tool for Sarathi Agent
Provides financial insights, earnings tracking, and expense management for drivers.
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models import Trip, Vehicle


class FinancialTool:
    """Tool for financial analysis and management"""
    
    async def calculate_earnings(
        self,
        user_id: int,
        db: Session,
        period: str = "week"
    ) -> Dict[str, Any]:
        """
        Calculate earnings for a specific period.
        
        Args:
            user_id: User ID
            db: Database session
            period: Time period (day, week, month, year)
        
        Returns:
            Earnings summary
        """
        # Calculate date range
        now = datetime.utcnow()
        if period == "day":
            start_date = now - timedelta(days=1)
        elif period == "week":
            start_date = now - timedelta(weeks=1)
        elif period == "month":
            start_date = now - timedelta(days=30)
        else:  # year
            start_date = now - timedelta(days=365)
        
        # Query trips
        trips = db.query(Trip).filter(
            Trip.user_id == user_id,
            Trip.trip_date >= start_date
        ).all()
        
        total_earnings = sum(trip.earnings for trip in trips)
        total_distance = sum(trip.distance_km for trip in trips)
        trip_count = len(trips)
        
        avg_earnings_per_trip = total_earnings / trip_count if trip_count > 0 else 0
        avg_earnings_per_km = total_earnings / total_distance if total_distance > 0 else 0
        
        return {
            "success": True,
            "period": period,
            "total_earnings": round(total_earnings, 2),
            "total_distance_km": round(total_distance, 2),
            "trip_count": trip_count,
            "avg_earnings_per_trip": round(avg_earnings_per_trip, 2),
            "avg_earnings_per_km": round(avg_earnings_per_km, 2)
        }
    
    async def project_fuel_costs(
        self,
        distance_km: float,
        vehicle_type: str = "car",
        fuel_price_per_liter: float = 1.5
    ) -> Dict[str, Any]:
        """
        Project fuel costs for a trip.
        
        Args:
            distance_km: Distance in kilometers
            vehicle_type: Type of vehicle
            fuel_price_per_liter: Current fuel price
        
        Returns:
            Fuel cost projection
        """
        # Average fuel efficiency (km per liter) by vehicle type
        fuel_efficiency = {
            "car": 12.0,
            "suv": 10.0,
            "motorcycle": 25.0,
            "truck": 8.0
        }
        
        efficiency = fuel_efficiency.get(vehicle_type.lower(), 12.0)
        fuel_needed = distance_km / efficiency
        total_cost = fuel_needed * fuel_price_per_liter
        
        return {
            "success": True,
            "distance_km": distance_km,
            "vehicle_type": vehicle_type,
            "fuel_efficiency_km_per_liter": efficiency,
            "fuel_needed_liters": round(fuel_needed, 2),
            "fuel_price_per_liter": fuel_price_per_liter,
            "estimated_cost": round(total_cost, 2)
        }
    
    async def calculate_profitability(
        self,
        trip_earnings: float,
        distance_km: float,
        vehicle_type: str = "car",
        fuel_price_per_liter: float = 1.5
    ) -> Dict[str, Any]:
        """
        Calculate trip profitability after expenses.
        
        Args:
            trip_earnings: Expected earnings from trip
            distance_km: Trip distance
            vehicle_type: Type of vehicle
            fuel_price_per_liter: Current fuel price
        
        Returns:
            Profitability analysis
        """
        fuel_costs = await self.project_fuel_costs(
            distance_km, vehicle_type, fuel_price_per_liter
        )
        
        # Additional costs (estimated)
        maintenance_cost_per_km = 0.05  # Average maintenance cost
        maintenance_cost = distance_km * maintenance_cost_per_km
        
        total_expenses = fuel_costs["estimated_cost"] + maintenance_cost
        net_profit = trip_earnings - total_expenses
        profit_margin = (net_profit / trip_earnings * 100) if trip_earnings > 0 else 0
        
        return {
            "success": True,
            "trip_earnings": round(trip_earnings, 2),
            "fuel_cost": round(fuel_costs["estimated_cost"], 2),
            "maintenance_cost": round(maintenance_cost, 2),
            "total_expenses": round(total_expenses, 2),
            "net_profit": round(net_profit, 2),
            "profit_margin_percent": round(profit_margin, 2),
            "recommendation": "Profitable trip" if net_profit > 0 else "Loss-making trip"
        }
    
    async def get_financial_insights(
        self,
        user_id: int,
        db: Session
    ) -> Dict[str, Any]:
        """
        Generate comprehensive financial insights.
        
        Args:
            user_id: User ID
            db: Database session
        
        Returns:
            Financial insights and recommendations
        """
        # Get earnings for different periods
        daily = await self.calculate_earnings(user_id, db, "day")
        weekly = await self.calculate_earnings(user_id, db, "week")
        monthly = await self.calculate_earnings(user_id, db, "month")
        
        insights = {
            "success": True,
            "daily_earnings": daily["total_earnings"],
            "weekly_earnings": weekly["total_earnings"],
            "monthly_earnings": monthly["total_earnings"],
            "weekly_trend": "increasing" if weekly["total_earnings"] > 0 else "stable",
            "recommendations": []
        }
        
        # Generate recommendations
        if weekly["avg_earnings_per_km"] > 0:
            insights["recommendations"].append(
                f"Your average earning is ${weekly['avg_earnings_per_km']:.2f} per km. "
                "Focus on longer trips for better profitability."
            )
        
        if weekly["trip_count"] < 10:
            insights["recommendations"].append(
                "Consider increasing your trip frequency to boost earnings."
            )
        
        return insights


# Tool instance
financial_tool = FinancialTool()
