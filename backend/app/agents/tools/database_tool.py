from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from app.models.trip import Trip
from app.models.vehicle import Vehicle, VehicleHealthCheck
from app.models.goal import Goal
from app.models.investment import Investment
from app.models.alert import Alert


class DatabaseTool:
    """Tool for querying database"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_trip_history(
        self,
        user_id: int,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get trip history for user"""
        start_date = datetime.now() - timedelta(days=days)
        
        result = await self.db.execute(
            select(Trip)
            .filter(Trip.user_id == user_id)
            .filter(Trip.created_at >= start_date)
            .order_by(Trip.created_at.desc())
        )
        
        trips = result.scalars().all()
        
        return [
            {
                'id': trip.id,
                'start_location': trip.start_location,
                'end_location': trip.end_location,
                'earnings': trip.earnings,
                'net_earnings': trip.net_earnings,
                'distance_km': trip.distance_km,
                'duration_minutes': trip.duration_minutes,
                'created_at': trip.created_at.isoformat(),
                'is_high_value_zone': trip.is_high_value_zone,
                'zone_rating': trip.zone_rating
            }
            for trip in trips
        ]
    
    async def get_trip_stats(
        self,
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get aggregated trip statistics"""
        start_date = datetime.now() - timedelta(days=days)
        
        result = await self.db.execute(
            select(
                func.count(Trip.id).label('total_trips'),
                func.sum(Trip.earnings).label('total_earnings'),
                func.sum(Trip.fuel_cost + Trip.toll_cost + Trip.other_expenses).label('total_expenses'),
                func.avg(Trip.earnings).label('avg_earnings')
            )
            .filter(Trip.user_id == user_id)
            .filter(Trip.created_at >= start_date)
        )
        
        stats = result.first()
        
        return {
            'total_trips': stats.total_trips or 0,
            'total_earnings': float(stats.total_earnings or 0),
            'total_expenses': float(stats.total_expenses or 0),
            'avg_earnings': float(stats.avg_earnings or 0),
            'net_earnings': float(stats.total_earnings or 0) - float(stats.total_expenses or 0)
        }
    
    async def get_vehicle_info(self, user_id: int) -> Dict[str, Any]:
        """Get vehicle information"""
        result = await self.db.execute(
            select(Vehicle)
            .filter(Vehicle.user_id == user_id)
            .filter(Vehicle.is_active == True)
        )
        
        vehicle = result.scalar_one_or_none()
        
        if not vehicle:
            return {}
        
        return {
            'id': vehicle.id,
            'vehicle_number': vehicle.vehicle_number,
            'vehicle_type': vehicle.vehicle_type,
            'make': vehicle.make,
            'model': vehicle.model,
            'current_odometer_km': vehicle.current_odometer_km,
            'insurance_expiry': vehicle.insurance_expiry.isoformat() if vehicle.insurance_expiry else None,
            'last_service_date': vehicle.last_service_date.isoformat() if vehicle.last_service_date else None,
            'next_service_due_km': vehicle.next_service_due_km
        }
    
    async def get_latest_vehicle_check(self, user_id: int) -> Dict[str, Any]:
        """Get latest vehicle health check"""
        result = await self.db.execute(
            select(VehicleHealthCheck)
            .join(Vehicle)
            .filter(Vehicle.user_id == user_id)
            .order_by(VehicleHealthCheck.created_at.desc())
            .limit(1)
        )
        
        check = result.scalar_one_or_none()
        
        if not check:
            return {}
        
        return {
            'id': check.id,
            'check_type': check.check_type,
            'severity_score': check.severity_score,
            'tire_condition': check.tire_condition,
            'engine_oil_level': check.engine_oil_level,
            'brake_condition': check.brake_condition,
            'immediate_action_required': check.immediate_action_required,
            'recommendations': check.recommendations,
            'created_at': check.created_at.isoformat()
        }
    
    async def get_goals(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user goals"""
        result = await self.db.execute(
            select(Goal)
            .filter(Goal.user_id == user_id)
            .filter(Goal.status.in_(['in_progress', 'completed']))
        )
        
        goals = result.scalars().all()
        
        return [
            {
                'id': goal.id,
                'goal_name': goal.goal_name,
                'target_amount': goal.target_amount,
                'current_amount': goal.current_amount,
                'completion_percentage': goal.percentage_complete,
                'target_date': goal.target_date.isoformat() if goal.target_date else None,
                'status': goal.status
            }
            for goal in goals
        ]
    
    async def get_investments(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user investments"""
        result = await self.db.execute(
            select(Investment)
            .filter(Investment.user_id == user_id)
            .filter(Investment.status == 'active')
        )
        
        investments = result.scalars().all()
        
        return [
            {
                'id': inv.id,
                'investment_name': inv.investment_name,
                'investment_type': inv.investment_type,
                'current_value': inv.current_value,
                'invested_amount': inv.invested_amount,
                'returns_percentage': inv.returns_percentage,
                'risk_level': inv.risk_level
            }
            for inv in investments
        ]
    
    async def get_active_alerts(self, user_id: int) -> List[Dict[str, Any]]:
        """Get active alerts"""
        result = await self.db.execute(
            select(Alert)
            .filter(Alert.user_id == user_id)
            .filter(Alert.status == 'active')
            .order_by(Alert.created_at.desc())
            .limit(10)
        )
        
        alerts = result.scalars().all()
        
        return [
            {
                'id': alert.id,
                'alert_type': alert.alert_type,
                'title': alert.title,
                'message': alert.message,
                'priority': alert.priority,
                'created_at': alert.created_at.isoformat()
            }
            for alert in alerts
        ]
