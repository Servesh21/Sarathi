"""
Real-time Event-Driven Architecture for Sarathi Guardian System
Implements proactive monitoring, event processing, and autonomous interventions
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
import redis.asyncio as redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic import BaseModel, Field
import uuid

# Internal imports
from ..guardian.resilience_system import resilience_guardian, ResilienceLevel, InterventionUrgency
from ..analytics.predictive_engine import analytics_engine
from ..knowledge.rag_system import knowledge_base
from ..graphs.advanced_orchestrator import guardian_agent

logger = logging.getLogger(__name__)

class EventType(Enum):
    """Types of system events"""
    # Critical events (immediate intervention required)
    VEHICLE_CRITICAL = "vehicle_critical"
    HEALTH_EMERGENCY = "health_emergency"
    FINANCIAL_CRISIS = "financial_crisis"
    SAFETY_ALERT = "safety_alert"
    
    # Warning events (intervention recommended)
    VEHICLE_WARNING = "vehicle_warning"
    BURNOUT_WARNING = "burnout_warning"
    EARNINGS_DROP = "earnings_drop"
    MAINTENANCE_DUE = "maintenance_due"
    
    # Opportunity events (optimization available)
    SURGE_DETECTED = "surge_detected"
    HIGH_DEMAND = "high_demand"
    WEATHER_OPPORTUNITY = "weather_opportunity"
    SAVINGS_OPPORTUNITY = "savings_opportunity"
    
    # Monitoring events (background tracking)
    TRIP_COMPLETED = "trip_completed"
    RESILIENCE_CHECK = "resilience_check"
    PERFORMANCE_METRIC = "performance_metric"
    USER_INTERACTION = "user_interaction"

class EventSeverity(Enum):
    """Event severity levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class SarathiEvent:
    """Sarathi system event structure"""
    event_id: str
    event_type: EventType
    severity: EventSeverity
    user_id: str
    timestamp: datetime
    data: Dict[str, Any]
    context: Dict[str, Any]
    auto_process: bool = True
    requires_intervention: bool = False
    intervention_deadline: Optional[datetime] = None

class EventProcessor:
    """Main event processing engine"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = None
        self.redis_url = redis_url
        self.event_handlers: Dict[EventType, List[Callable]] = {}
        self.scheduler = AsyncIOScheduler()
        self.active_monitors = {}
        self.event_queue = asyncio.Queue()
        
        # Register default event handlers
        self._register_default_handlers()
        
        logger.info("Event Processor initialized")
    
    async def initialize(self):
        """Initialize Redis connection and start scheduler"""
        try:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
            await self.redis_client.ping()
            self.scheduler.start()
            
            # Start background event processing
            asyncio.create_task(self._process_event_queue())
            
            logger.info("Event system initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize event system: {str(e)}")
            # Fallback to in-memory processing
            self.redis_client = None
    
    def register_handler(self, event_type: EventType, handler: Callable):
        """Register an event handler"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    async def emit_event(self, event: SarathiEvent):
        """Emit an event for processing"""
        try:
            # Add to queue for processing
            await self.event_queue.put(event)
            
            # Also publish to Redis if available for external subscribers
            if self.redis_client:
                await self.redis_client.publish(
                    f"sarathi_events_{event.user_id}",
                    json.dumps(asdict(event), default=str)
                )
            
            logger.info(f"Event emitted: {event.event_type.value} for user {event.user_id}")
            
        except Exception as e:
            logger.error(f"Error emitting event: {str(e)}")
    
    async def _process_event_queue(self):
        """Process events from the queue"""
        while True:
            try:
                # Get event from queue (blocks until available)
                event = await self.event_queue.get()
                
                # Process the event
                await self._process_event(event)
                
                # Mark task as done
                self.event_queue.task_done()
                
            except Exception as e:
                logger.error(f"Error processing event queue: {str(e)}")
                await asyncio.sleep(1)
    
    async def _process_event(self, event: SarathiEvent):
        """Process a single event"""
        try:
            # Log event processing
            logger.info(f"Processing event: {event.event_type.value} (severity: {event.severity.name})")
            
            # Check if immediate intervention is needed
            if event.severity == EventSeverity.CRITICAL:
                await self._handle_critical_event(event)
            
            # Run registered handlers
            handlers = self.event_handlers.get(event.event_type, [])
            for handler in handlers:
                try:
                    await handler(event)
                except Exception as handler_error:
                    logger.error(f"Error in event handler: {str(handler_error)}")
            
            # Store event for analytics
            await self._store_event(event)
            
        except Exception as e:
            logger.error(f"Error processing event {event.event_id}: {str(e)}")
    
    async def _handle_critical_event(self, event: SarathiEvent):
        """Handle critical events requiring immediate intervention"""
        try:
            # Generate immediate intervention
            user_data = await self._get_user_context(event.user_id)
            
            # Get resilience assessment
            resilience_metrics = await resilience_guardian.assess_resilience(user_data)
            
            # Generate interventions
            interventions = await resilience_guardian.generate_interventions(user_data, resilience_metrics)
            
            # Execute autonomous actions for critical events
            critical_interventions = [i for i in interventions if i.urgency == InterventionUrgency.CRITICAL]
            
            if critical_interventions:
                await resilience_guardian.execute_autonomous_actions(event.user_id, critical_interventions)
                
                # Create notification event
                notification_event = SarathiEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=EventType.SAFETY_ALERT,
                    severity=EventSeverity.CRITICAL,
                    user_id=event.user_id,
                    timestamp=datetime.now(),
                    data={
                        'message': 'Critical intervention executed',
                        'interventions': len(critical_interventions),
                        'original_event': event.event_type.value
                    },
                    context={'auto_executed': True}
                )
                
                await self.emit_event(notification_event)
            
            logger.info(f"Critical event handled for user {event.user_id}")
            
        except Exception as e:
            logger.error(f"Error handling critical event: {str(e)}")
    
    def _register_default_handlers(self):
        """Register default event handlers"""
        
        # Vehicle health handlers
        self.register_handler(EventType.VEHICLE_CRITICAL, self._handle_vehicle_critical)
        self.register_handler(EventType.VEHICLE_WARNING, self._handle_vehicle_warning)
        self.register_handler(EventType.MAINTENANCE_DUE, self._handle_maintenance_due)
        
        # Health and burnout handlers
        self.register_handler(EventType.HEALTH_EMERGENCY, self._handle_health_emergency)
        self.register_handler(EventType.BURNOUT_WARNING, self._handle_burnout_warning)
        
        # Financial handlers
        self.register_handler(EventType.FINANCIAL_CRISIS, self._handle_financial_crisis)
        self.register_handler(EventType.EARNINGS_DROP, self._handle_earnings_drop)
        self.register_handler(EventType.SAVINGS_OPPORTUNITY, self._handle_savings_opportunity)
        
        # Opportunity handlers
        self.register_handler(EventType.SURGE_DETECTED, self._handle_surge_detected)
        self.register_handler(EventType.HIGH_DEMAND, self._handle_high_demand)
        self.register_handler(EventType.WEATHER_OPPORTUNITY, self._handle_weather_opportunity)
        
        # Monitoring handlers
        self.register_handler(EventType.TRIP_COMPLETED, self._handle_trip_completed)
        self.register_handler(EventType.RESILIENCE_CHECK, self._handle_resilience_check)
    
    # Event handler methods
    async def _handle_vehicle_critical(self, event: SarathiEvent):
        """Handle critical vehicle health events"""
        vehicle_data = event.data.get('vehicle_data', {})
        
        # Create immediate alert
        alert_message = f"🚨 CRITICAL: Vehicle issue detected. {vehicle_data.get('issue_description', 'Immediate attention required.')}"
        
        # Schedule emergency service if auto-executable
        if event.auto_process:
            # Find nearby emergency services
            emergency_services = await self._find_emergency_services(event.user_id)
            
            # Log the intervention
            logger.critical(f"Vehicle critical event for user {event.user_id}: {alert_message}")
    
    async def _handle_vehicle_warning(self, event: SarathiEvent):
        """Handle vehicle warning events"""
        vehicle_data = event.data.get('vehicle_data', {})
        
        # Schedule maintenance reminder
        maintenance_due = datetime.now() + timedelta(days=3)
        
        await self._schedule_reminder(
            event.user_id,
            "vehicle_maintenance",
            maintenance_due,
            f"Schedule vehicle maintenance: {vehicle_data.get('warning_description', 'General maintenance needed')}"
        )
    
    async def _handle_maintenance_due(self, event: SarathiEvent):
        """Handle maintenance due events"""
        maintenance_data = event.data.get('maintenance_data', {})
        
        # Calculate optimal maintenance timing
        optimal_time = await self._calculate_optimal_maintenance_time(event.user_id, maintenance_data)
        
        # Create proactive intervention
        logger.info(f"Maintenance due for user {event.user_id} - optimal timing: {optimal_time}")
    
    async def _handle_health_emergency(self, event: SarathiEvent):
        """Handle driver health emergencies"""
        health_data = event.data.get('health_data', {})
        
        # Force rest period
        await self._enforce_rest_period(event.user_id, hours=24)
        
        # Alert emergency contact if available
        await self._alert_emergency_contact(event.user_id, health_data)
        
        logger.critical(f"Health emergency for user {event.user_id}")
    
    async def _handle_burnout_warning(self, event: SarathiEvent):
        """Handle burnout warning events"""
        burnout_data = event.data.get('burnout_data', {})
        
        # Schedule mandatory rest days
        rest_days = burnout_data.get('recommended_rest_days', 2)
        await self._schedule_rest_days(event.user_id, rest_days)
        
        logger.warning(f"Burnout warning for user {event.user_id} - {rest_days} rest days scheduled")
    
    async def _handle_financial_crisis(self, event: SarathiEvent):
        """Handle financial crisis events"""
        financial_data = event.data.get('financial_data', {})
        
        # Enable emergency mode
        await self._enable_emergency_mode(event.user_id)
        
        # Suggest immediate income opportunities
        opportunities = await self._find_immediate_income_opportunities(event.user_id)
        
        logger.critical(f"Financial crisis for user {event.user_id} - emergency mode enabled")
    
    async def _handle_earnings_drop(self, event: SarathiEvent):
        """Handle earnings drop events"""
        earnings_data = event.data.get('earnings_data', {})
        
        # Analyze earnings patterns
        patterns = await analytics_engine.earnings_optimizer.optimize_earnings(
            {'user_id': event.user_id},
            {'current_earnings': earnings_data}
        )
        
        # Create optimization plan
        optimization_plan = {
            'optimal_hours': patterns.optimal_hours,
            'recommended_locations': patterns.location_recommendations,
            'expected_improvement': patterns.predicted_daily_earnings - earnings_data.get('current_daily', 0)
        }
        
        logger.info(f"Earnings optimization planned for user {event.user_id}")
    
    async def _handle_surge_detected(self, event: SarathiEvent):
        """Handle surge pricing opportunities"""
        surge_data = event.data.get('surge_data', {})
        
        # Send real-time notification
        notification = {
            'title': '💰 Surge Detected!',
            'message': f"Surge of {surge_data.get('multiplier', '1.5')}x detected in {surge_data.get('area', 'your area')}",
            'urgency': 'high',
            'expires_at': datetime.now() + timedelta(minutes=30)
        }
        
        await self._send_realtime_notification(event.user_id, notification)
    
    async def _handle_high_demand(self, event: SarathiEvent):
        """Handle high demand opportunities"""
        demand_data = event.data.get('demand_data', {})
        
        # Calculate potential earnings increase
        potential_increase = demand_data.get('potential_increase', 0.3)  # 30% increase
        
        # Send optimization suggestion
        suggestion = {
            'message': f"High demand detected - potential {potential_increase*100:.0f}% earnings increase",
            'recommended_action': 'Move to high-demand areas',
            'locations': demand_data.get('high_demand_areas', []),
            'duration': demand_data.get('expected_duration', '2 hours')
        }
        
        await self._send_optimization_suggestion(event.user_id, suggestion)
    
    async def _handle_weather_opportunity(self, event: SarathiEvent):
        """Handle weather-based opportunities"""
        weather_data = event.data.get('weather_data', {})
        
        if weather_data.get('rain_probability', 0) > 0.7:
            # Rain opportunity
            opportunity = {
                'type': 'rain_surge',
                'message': 'Rain predicted - surge pricing likely',
                'recommended_strategy': 'Position near covered pickup points',
                'expected_benefit': '20-50% higher fares',
                'duration': weather_data.get('rain_duration', 'Next 2-4 hours')
            }
        else:
            # Other weather opportunities
            opportunity = {
                'type': 'weather_based',
                'message': f"Weather impact detected: {weather_data.get('condition', 'Unknown')}",
                'recommended_strategy': weather_data.get('strategy', 'Adjust driving pattern'),
                'expected_benefit': weather_data.get('benefit', 'Optimized earnings')
            }
        
        await self._send_weather_opportunity(event.user_id, opportunity)
    
    async def _handle_trip_completed(self, event: SarathiEvent):
        """Handle trip completion events"""
        trip_data = event.data.get('trip_data', {})
        
        # Update real-time analytics
        await self._update_realtime_analytics(event.user_id, trip_data)
        
        # Check for patterns
        patterns = await self._analyze_trip_patterns(event.user_id, trip_data)
        
        if patterns.get('efficiency_drop', False):
            # Efficiency dropping - suggest optimization
            optimization_event = SarathiEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.EARNINGS_DROP,
                severity=EventSeverity.MEDIUM,
                user_id=event.user_id,
                timestamp=datetime.now(),
                data={'earnings_data': patterns},
                context={'triggered_by': 'trip_analysis'}
            )
            await self.emit_event(optimization_event)
    
    async def _handle_resilience_check(self, event: SarathiEvent):
        """Handle periodic resilience assessments"""
        user_data = await self._get_user_context(event.user_id)
        
        # Perform comprehensive resilience assessment
        resilience_metrics = await resilience_guardian.assess_resilience(user_data)
        
        # Check if resilience level changed
        previous_level = event.data.get('previous_resilience_level')
        current_level = self._get_resilience_level(resilience_metrics.overall_score)
        
        if current_level != previous_level:
            # Resilience level changed
            level_change_event = SarathiEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.PERFORMANCE_METRIC,
                severity=EventSeverity.MEDIUM,
                user_id=event.user_id,
                timestamp=datetime.now(),
                data={
                    'metric': 'resilience_level_change',
                    'previous_level': previous_level,
                    'current_level': current_level.value,
                    'resilience_score': resilience_metrics.overall_score
                },
                context={'auto_generated': True}
            )
            await self.emit_event(level_change_event)
    
    # Utility methods
    async def _get_user_context(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user context"""
        # This would fetch from database and other sources
        # For now, return mock context
        return {
            'user_id': user_id,
            'driver': {
                'daily_hours_avg': 10,
                'consecutive_work_days': 7,
                'daily_earnings_avg': 1200,
                'sleep_hours': 6,
                'stress_level': 6
            },
            'vehicle': {
                'mileage': 85000,
                'km_since_last_service': 4200,
                'age_in_months': 48,
                'health_score': 75
            },
            'financial': {
                'monthly_income_avg': 36000,
                'emergency_fund': 18000,
                'savings_rate': 0.18
            }
        }
    
    def _get_resilience_level(self, score: float) -> ResilienceLevel:
        """Convert resilience score to level"""
        if score >= 80:
            return ResilienceLevel.ANTIFRAGILE
        elif score >= 65:
            return ResilienceLevel.RESILIENT
        elif score >= 50:
            return ResilienceLevel.STABLE
        elif score >= 35:
            return ResilienceLevel.VULNERABLE
        else:
            return ResilienceLevel.FRAGILE
    
    async def _store_event(self, event: SarathiEvent):
        """Store event for analytics and learning"""
        try:
            # Store in Redis for real-time access
            if self.redis_client:
                key = f"events:{event.user_id}:{datetime.now().strftime('%Y%m%d')}"
                await self.redis_client.lpush(key, json.dumps(asdict(event), default=str))
                await self.redis_client.expire(key, 86400 * 7)  # Keep for 7 days
            
            # Here you would also store in main database
            logger.debug(f"Event stored: {event.event_id}")
            
        except Exception as e:
            logger.error(f"Error storing event: {str(e)}")
    
    # Placeholder methods for specific actions
    async def _find_emergency_services(self, user_id: str) -> List[Dict]:
        """Find emergency vehicle services"""
        return []
    
    async def _schedule_reminder(self, user_id: str, reminder_type: str, when: datetime, message: str):
        """Schedule a reminder"""
        logger.info(f"Reminder scheduled for {user_id}: {message}")
    
    async def _calculate_optimal_maintenance_time(self, user_id: str, maintenance_data: Dict) -> datetime:
        """Calculate optimal maintenance timing"""
        return datetime.now() + timedelta(days=2)
    
    async def _enforce_rest_period(self, user_id: str, hours: int):
        """Enforce rest period"""
        logger.critical(f"Enforcing {hours}h rest for user {user_id}")
    
    async def _alert_emergency_contact(self, user_id: str, health_data: Dict):
        """Alert emergency contact"""
        logger.critical(f"Alerting emergency contact for user {user_id}")
    
    async def _schedule_rest_days(self, user_id: str, days: int):
        """Schedule rest days"""
        logger.warning(f"Scheduling {days} rest days for user {user_id}")
    
    async def _enable_emergency_mode(self, user_id: str):
        """Enable emergency financial mode"""
        logger.critical(f"Emergency mode enabled for user {user_id}")
    
    async def _find_immediate_income_opportunities(self, user_id: str) -> List[Dict]:
        """Find immediate income opportunities"""
        return []
    
    async def _send_realtime_notification(self, user_id: str, notification: Dict):
        """Send real-time notification"""
        logger.info(f"Real-time notification sent to {user_id}: {notification['title']}")
    
    async def _send_optimization_suggestion(self, user_id: str, suggestion: Dict):
        """Send optimization suggestion"""
        logger.info(f"Optimization suggestion sent to {user_id}")
    
    async def _send_weather_opportunity(self, user_id: str, opportunity: Dict):
        """Send weather opportunity notification"""
        logger.info(f"Weather opportunity sent to {user_id}: {opportunity['type']}")
    
    async def _update_realtime_analytics(self, user_id: str, trip_data: Dict):
        """Update real-time analytics"""
        logger.debug(f"Analytics updated for user {user_id}")
    
    async def _analyze_trip_patterns(self, user_id: str, trip_data: Dict) -> Dict:
        """Analyze trip patterns"""
        return {'efficiency_drop': False}


class RealTimeMonitor:
    """Real-time monitoring system"""
    
    def __init__(self, event_processor: EventProcessor):
        self.event_processor = event_processor
        self.monitoring_tasks = {}
        self.scheduler = AsyncIOScheduler()
    
    async def start_monitoring(self, user_id: str, monitoring_config: Dict[str, Any]):
        """Start monitoring for a user"""
        try:
            # Stop existing monitoring if any
            await self.stop_monitoring(user_id)
            
            # Create monitoring task
            task = asyncio.create_task(self._monitor_user(user_id, monitoring_config))
            self.monitoring_tasks[user_id] = task
            
            logger.info(f"Started monitoring for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error starting monitoring for user {user_id}: {str(e)}")
    
    async def stop_monitoring(self, user_id: str):
        """Stop monitoring for a user"""
        try:
            if user_id in self.monitoring_tasks:
                self.monitoring_tasks[user_id].cancel()
                del self.monitoring_tasks[user_id]
                logger.info(f"Stopped monitoring for user {user_id}")
        except Exception as e:
            logger.error(f"Error stopping monitoring for user {user_id}: {str(e)}")
    
    async def _monitor_user(self, user_id: str, config: Dict[str, Any]):
        """Monitor a specific user"""
        try:
            check_interval = config.get('check_interval_seconds', 300)  # Default 5 minutes
            
            while True:
                await asyncio.sleep(check_interval)
                
                # Get current user state
                user_data = await self.event_processor._get_user_context(user_id)
                
                # Check various conditions
                await self._check_vehicle_health(user_id, user_data)
                await self._check_driver_health(user_id, user_data)
                await self._check_financial_health(user_id, user_data)
                await self._check_earning_opportunities(user_id, user_data)
                
        except asyncio.CancelledError:
            logger.info(f"Monitoring cancelled for user {user_id}")
        except Exception as e:
            logger.error(f"Error monitoring user {user_id}: {str(e)}")
    
    async def _check_vehicle_health(self, user_id: str, user_data: Dict[str, Any]):
        """Check vehicle health and emit events if needed"""
        vehicle_data = user_data.get('vehicle', {})
        
        health_score = vehicle_data.get('health_score', 100)
        km_since_service = vehicle_data.get('km_since_last_service', 0)
        
        if health_score < 30:
            # Critical vehicle health
            event = SarathiEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.VEHICLE_CRITICAL,
                severity=EventSeverity.CRITICAL,
                user_id=user_id,
                timestamp=datetime.now(),
                data={'vehicle_data': vehicle_data},
                context={'triggered_by': 'monitoring'}
            )
            await self.event_processor.emit_event(event)
            
        elif health_score < 60 or km_since_service > 5000:
            # Warning level
            event = SarathiEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.VEHICLE_WARNING,
                severity=EventSeverity.HIGH,
                user_id=user_id,
                timestamp=datetime.now(),
                data={'vehicle_data': vehicle_data},
                context={'triggered_by': 'monitoring'}
            )
            await self.event_processor.emit_event(event)
    
    async def _check_driver_health(self, user_id: str, user_data: Dict[str, Any]):
        """Check driver health and burnout"""
        driver_data = user_data.get('driver', {})
        
        consecutive_days = driver_data.get('consecutive_work_days', 0)
        daily_hours = driver_data.get('daily_hours_avg', 8)
        sleep_hours = driver_data.get('sleep_hours', 7)
        
        # Critical health check
        if consecutive_days > 14 or daily_hours > 16 or sleep_hours < 4:
            event = SarathiEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.HEALTH_EMERGENCY,
                severity=EventSeverity.CRITICAL,
                user_id=user_id,
                timestamp=datetime.now(),
                data={'health_data': driver_data},
                context={'triggered_by': 'monitoring'}
            )
            await self.event_processor.emit_event(event)
            
        # Burnout warning
        elif consecutive_days > 10 or daily_hours > 12 or sleep_hours < 6:
            event = SarathiEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.BURNOUT_WARNING,
                severity=EventSeverity.HIGH,
                user_id=user_id,
                timestamp=datetime.now(),
                data={'burnout_data': driver_data},
                context={'triggered_by': 'monitoring'}
            )
            await self.event_processor.emit_event(event)
    
    async def _check_financial_health(self, user_id: str, user_data: Dict[str, Any]):
        """Check financial health"""
        financial_data = user_data.get('financial', {})
        
        emergency_fund = financial_data.get('emergency_fund', 0)
        monthly_expenses = financial_data.get('monthly_expenses_avg', 25000)
        
        if emergency_fund < monthly_expenses * 0.5:  # Less than 2 weeks expenses
            event = SarathiEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.FINANCIAL_CRISIS,
                severity=EventSeverity.CRITICAL,
                user_id=user_id,
                timestamp=datetime.now(),
                data={'financial_data': financial_data},
                context={'triggered_by': 'monitoring'}
            )
            await self.event_processor.emit_event(event)
    
    async def _check_earning_opportunities(self, user_id: str, user_data: Dict[str, Any]):
        """Check for earning opportunities"""
        # This would connect to real-time data sources
        # For now, simulate opportunity detection
        
        current_hour = datetime.now().hour
        if current_hour in [8, 18, 19]:  # Peak hours
            # Simulate surge detection
            if random_chance := True:  # Placeholder for real surge detection
                event = SarathiEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=EventType.SURGE_DETECTED,
                    severity=EventSeverity.MEDIUM,
                    user_id=user_id,
                    timestamp=datetime.now(),
                    data={
                        'surge_data': {
                            'multiplier': 1.4,
                            'area': 'Business District',
                            'duration_estimate': 30
                        }
                    },
                    context={'triggered_by': 'monitoring'}
                )
                await self.event_processor.emit_event(event)


# Global instances
event_processor = EventProcessor()
realtime_monitor = RealTimeMonitor(event_processor)