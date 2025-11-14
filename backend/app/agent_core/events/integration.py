"""
Event Integration Module for Sarathi Guardian System
Integrates event processing with the main agent orchestrator and API endpoints
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
import json
import uuid

# Internal imports
from .realtime_system import event_processor, realtime_monitor, SarathiEvent, EventType, EventSeverity
from .alert_system import alert_manager, emergency_system, AlertPriority, AlertChannel
from ..graphs.advanced_orchestrator import guardian_agent
from ..guardian.resilience_system import resilience_guardian
from ...core.config import settings

logger = logging.getLogger(__name__)

# Pydantic models for API
class EventRequest(BaseModel):
    event_type: str = Field(..., description="Type of event")
    severity: str = Field(..., description="Event severity level")
    data: Dict[str, Any] = Field(default_factory=dict, description="Event data")
    context: Dict[str, Any] = Field(default_factory=dict, description="Event context")
    user_id: str = Field(..., description="User ID")

class AlertPreferences(BaseModel):
    disabled_channels: List[str] = Field(default_factory=list)
    quiet_hours: Optional[Dict[str, int]] = None
    priority_threshold: str = Field(default="normal", description="Minimum priority for alerts")

class MonitoringConfig(BaseModel):
    check_interval_seconds: int = Field(default=300, description="Check interval in seconds")
    vehicle_health_threshold: int = Field(default=60, description="Vehicle health warning threshold")
    burnout_consecutive_days: int = Field(default=10, description="Consecutive days threshold for burnout")
    financial_emergency_ratio: float = Field(default=0.5, description="Emergency fund ratio threshold")

class WebSocketConnectionManager:
    """Manages WebSocket connections for real-time alerts"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, user_id: str):
        """Connect a new WebSocket client"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"WebSocket connected for user {user_id}")
    
    def disconnect(self, user_id: str):
        """Disconnect a WebSocket client"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"WebSocket disconnected for user {user_id}")
    
    async def send_to_user(self, user_id: str, message: dict):
        """Send message to specific user"""
        websocket = self.active_connections.get(user_id)
        if websocket:
            try:
                await websocket.send_text(json.dumps(message, default=str))
                return True
            except Exception as e:
                logger.error(f"Error sending WebSocket message to {user_id}: {str(e)}")
                self.disconnect(user_id)
        return False

# Global WebSocket manager
connection_manager = WebSocketConnectionManager()

class EventIntegrationService:
    """Main service for integrating events with the guardian system"""
    
    def __init__(self):
        self.is_initialized = False
        self.background_tasks: List[asyncio.Task] = []
        
    async def initialize(self):
        """Initialize the event integration service"""
        try:
            # Initialize event processor
            await event_processor.initialize()
            
            # Register event handlers for agent integration
            self._register_agent_integration_handlers()
            
            # Register alert generation handlers
            self._register_alert_generation_handlers()
            
            # Start background tasks
            self._start_background_tasks()
            
            self.is_initialized = True
            logger.info("Event Integration Service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Event Integration Service: {str(e)}")
            raise e
    
    def _register_agent_integration_handlers(self):
        """Register handlers that integrate events with the AI agent system"""
        
        # Critical events that trigger guardian intervention
        event_processor.register_handler(EventType.VEHICLE_CRITICAL, self._handle_guardian_intervention)
        event_processor.register_handler(EventType.HEALTH_EMERGENCY, self._handle_guardian_intervention)
        event_processor.register_handler(EventType.FINANCIAL_CRISIS, self._handle_guardian_intervention)
        
        # Learning events that update agent knowledge
        event_processor.register_handler(EventType.TRIP_COMPLETED, self._handle_learning_update)
        event_processor.register_handler(EventType.USER_INTERACTION, self._handle_learning_update)
        
        # Optimization events that trigger proactive suggestions
        event_processor.register_handler(EventType.SURGE_DETECTED, self._handle_optimization_trigger)
        event_processor.register_handler(EventType.HIGH_DEMAND, self._handle_optimization_trigger)
        event_processor.register_handler(EventType.WEATHER_OPPORTUNITY, self._handle_optimization_trigger)
    
    def _register_alert_generation_handlers(self):
        """Register handlers that generate alerts from events"""
        
        # All events that should generate alerts
        for event_type in EventType:
            if event_type not in [EventType.PERFORMANCE_METRIC, EventType.USER_INTERACTION]:
                event_processor.register_handler(event_type, self._generate_alert_from_event)
    
    def _start_background_tasks(self):
        """Start background monitoring tasks"""
        
        # Periodic resilience assessments
        task1 = asyncio.create_task(self._periodic_resilience_check())
        self.background_tasks.append(task1)
        
        # WebSocket heartbeat
        task2 = asyncio.create_task(self._websocket_heartbeat())
        self.background_tasks.append(task2)
        
        # Alert cleanup
        task3 = asyncio.create_task(self._cleanup_old_alerts())
        self.background_tasks.append(task3)
    
    # Event handler methods
    async def _handle_guardian_intervention(self, event: SarathiEvent):
        """Handle events that require guardian intervention"""
        try:
            logger.info(f"Guardian intervention triggered by event: {event.event_type.value}")
            
            # Get user context
            user_data = await event_processor._get_user_context(event.user_id)
            
            # Generate and execute interventions through the guardian agent
            response = await guardian_agent.ainvoke({
                'user_id': event.user_id,
                'context': user_data,
                'event_data': event.data,
                'intervention_type': 'emergency' if event.severity == EventSeverity.CRITICAL else 'proactive'
            })
            
            # Log intervention result
            logger.info(f"Guardian intervention completed for user {event.user_id}: {response.get('interventions_count', 0)} actions taken")
            
        except Exception as e:
            logger.error(f"Error in guardian intervention: {str(e)}")
    
    async def _handle_learning_update(self, event: SarathiEvent):
        """Handle events that update agent learning"""
        try:
            # Extract learning data from event
            learning_data = {
                'user_id': event.user_id,
                'event_type': event.event_type.value,
                'timestamp': event.timestamp,
                'data': event.data,
                'context': event.context
            }
            
            # Update knowledge base with new data
            await self._update_knowledge_base(learning_data)
            
            # Update user patterns
            await self._update_user_patterns(event.user_id, learning_data)
            
            logger.debug(f"Learning update processed for event: {event.event_id}")
            
        except Exception as e:
            logger.error(f"Error in learning update: {str(e)}")
    
    async def _handle_optimization_trigger(self, event: SarathiEvent):
        """Handle events that trigger optimization suggestions"""
        try:
            # Generate optimization suggestions through the agent
            optimization_response = await guardian_agent.ainvoke({
                'user_id': event.user_id,
                'task': 'optimization',
                'opportunity_data': event.data,
                'context': event.context
            })
            
            # Send optimization suggestions via WebSocket if user is connected
            if optimization_response.get('suggestions'):
                message = {
                    'type': 'optimization_suggestion',
                    'event_id': event.event_id,
                    'suggestions': optimization_response['suggestions'],
                    'priority': event.severity.value,
                    'expires_at': (datetime.now() + timedelta(hours=1)).isoformat()
                }
                
                await connection_manager.send_to_user(event.user_id, message)
            
            logger.info(f"Optimization suggestions sent for event: {event.event_type.value}")
            
        except Exception as e:
            logger.error(f"Error in optimization trigger: {str(e)}")
    
    async def _generate_alert_from_event(self, event: SarathiEvent):
        """Generate alert from event"""
        try:
            # Create alert from event
            alert = await alert_manager.create_alert_from_event(event)
            
            if alert:
                # Send alert through appropriate channels
                success = await alert_manager.send_alert(alert)
                
                if success:
                    # Also send to WebSocket if user is connected
                    ws_message = {
                        'type': 'alert',
                        'alert_id': alert.alert_id,
                        'title': alert.title,
                        'message': alert.message,
                        'priority': alert.priority.value,
                        'actions': alert.actions,
                        'created_at': alert.created_at.isoformat()
                    }
                    
                    await connection_manager.send_to_user(event.user_id, ws_message)
                
                logger.debug(f"Alert generated for event: {event.event_id}")
            
        except Exception as e:
            logger.error(f"Error generating alert from event: {str(e)}")
    
    # Background task methods
    async def _periodic_resilience_check(self):
        """Perform periodic resilience assessments for all active users"""
        while True:
            try:
                await asyncio.sleep(3600)  # Every hour
                
                # Get list of active users (this would come from database)
                active_users = await self._get_active_users()
                
                for user_id in active_users:
                    try:
                        # Create resilience check event
                        event = SarathiEvent(
                            event_id=str(uuid.uuid4()),
                            event_type=EventType.RESILIENCE_CHECK,
                            severity=EventSeverity.LOW,
                            user_id=user_id,
                            timestamp=datetime.now(),
                            data={'check_type': 'periodic'},
                            context={'automated': True}
                        )
                        
                        await event_processor.emit_event(event)
                        
                    except Exception as user_error:
                        logger.error(f"Error in resilience check for user {user_id}: {str(user_error)}")
                
            except Exception as e:
                logger.error(f"Error in periodic resilience check: {str(e)}")
    
    async def _websocket_heartbeat(self):
        """Send periodic heartbeat to connected WebSocket clients"""
        while True:
            try:
                await asyncio.sleep(30)  # Every 30 seconds
                
                disconnected_users = []
                for user_id in list(connection_manager.active_connections.keys()):
                    try:
                        websocket = connection_manager.active_connections[user_id]
                        await websocket.ping()
                    except Exception:
                        disconnected_users.append(user_id)
                
                # Clean up disconnected users
                for user_id in disconnected_users:
                    connection_manager.disconnect(user_id)
                
            except Exception as e:
                logger.error(f"Error in WebSocket heartbeat: {str(e)}")
    
    async def _cleanup_old_alerts(self):
        """Clean up old alerts and events"""
        while True:
            try:
                await asyncio.sleep(3600 * 6)  # Every 6 hours
                
                cutoff_time = datetime.now() - timedelta(days=7)
                
                # Clean up old alerts
                old_alert_ids = []
                for alert_id, alert in alert_manager.sent_alerts.items():
                    if alert.created_at < cutoff_time:
                        old_alert_ids.append(alert_id)
                
                for alert_id in old_alert_ids:
                    del alert_manager.sent_alerts[alert_id]
                
                logger.info(f"Cleaned up {len(old_alert_ids)} old alerts")
                
            except Exception as e:
                logger.error(f"Error in alert cleanup: {str(e)}")
    
    # Utility methods
    async def _update_knowledge_base(self, learning_data: Dict[str, Any]):
        """Update the knowledge base with new learning data"""
        try:
            # This would update the RAG knowledge base
            # For now, just log the learning data
            logger.debug(f"Knowledge base update: {learning_data['event_type']}")
        except Exception as e:
            logger.error(f"Error updating knowledge base: {str(e)}")
    
    async def _update_user_patterns(self, user_id: str, learning_data: Dict[str, Any]):
        """Update user behavior patterns"""
        try:
            # This would update user pattern models
            logger.debug(f"User patterns updated for {user_id}")
        except Exception as e:
            logger.error(f"Error updating user patterns: {str(e)}")
    
    async def _get_active_users(self) -> List[str]:
        """Get list of active users"""
        # This would query the database for active users
        # For now, return connected WebSocket users
        return list(connection_manager.active_connections.keys())
    
    async def emit_user_event(self, user_id: str, event_type: str, data: Dict[str, Any], 
                            severity: str = "medium", context: Dict[str, Any] = None):
        """Emit an event for a user"""
        try:
            event = SarathiEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType(event_type),
                severity=EventSeverity[severity.upper()],
                user_id=user_id,
                timestamp=datetime.now(),
                data=data,
                context=context or {}
            )
            
            await event_processor.emit_event(event)
            return True
            
        except Exception as e:
            logger.error(f"Error emitting user event: {str(e)}")
            return False
    
    async def start_user_monitoring(self, user_id: str, config: Dict[str, Any] = None):
        """Start monitoring for a user"""
        try:
            monitoring_config = config or {
                'check_interval_seconds': 300,
                'vehicle_health_threshold': 60,
                'burnout_consecutive_days': 10,
                'financial_emergency_ratio': 0.5
            }
            
            await realtime_monitor.start_monitoring(user_id, monitoring_config)
            return True
            
        except Exception as e:
            logger.error(f"Error starting user monitoring: {str(e)}")
            return False
    
    async def stop_user_monitoring(self, user_id: str):
        """Stop monitoring for a user"""
        try:
            await realtime_monitor.stop_monitoring(user_id)
            return True
            
        except Exception as e:
            logger.error(f"Error stopping user monitoring: {str(e)}")
            return False


# Global service instance
event_integration_service = EventIntegrationService()

# API Router
router = APIRouter(prefix="/events", tags=["events"])

@router.post("/emit")
async def emit_event(event_request: EventRequest, user_id: str = None):
    """Emit a new event"""
    try:
        target_user_id = user_id or event_request.user_id
        
        success = await event_integration_service.emit_user_event(
            user_id=target_user_id,
            event_type=event_request.event_type,
            data=event_request.data,
            severity=event_request.severity,
            context=event_request.context
        )
        
        if success:
            return {"status": "success", "message": "Event emitted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to emit event")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid event type or severity: {str(e)}")
    except Exception as e:
        logger.error(f"Error in emit_event endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/alerts/{user_id}")
async def get_user_alerts(user_id: str, status: Optional[str] = None, limit: int = 50):
    """Get alerts for a user"""
    try:
        status_filter = None
        if status:
            from .alert_system import AlertStatus
            status_filter = AlertStatus(status.upper())
        
        alerts = await alert_manager.get_user_alerts(user_id, status_filter, limit)
        
        return {
            "alerts": [
                {
                    "alert_id": alert.alert_id,
                    "title": alert.title,
                    "message": alert.message,
                    "priority": alert.priority.value,
                    "status": alert.status.value,
                    "created_at": alert.created_at.isoformat(),
                    "actions": alert.actions
                }
                for alert in alerts
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting user alerts: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str, user_id: str):
    """Acknowledge an alert"""
    try:
        success = await alert_manager.acknowledge_alert(alert_id, user_id)
        
        if success:
            return {"status": "success", "message": "Alert acknowledged"}
        else:
            raise HTTPException(status_code=404, detail="Alert not found or not accessible")
            
    except Exception as e:
        logger.error(f"Error acknowledging alert: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/alerts/{alert_id}/dismiss")
async def dismiss_alert(alert_id: str, user_id: str):
    """Dismiss an alert"""
    try:
        success = await alert_manager.dismiss_alert(alert_id, user_id)
        
        if success:
            return {"status": "success", "message": "Alert dismissed"}
        else:
            raise HTTPException(status_code=404, detail="Alert not found or not accessible")
            
    except Exception as e:
        logger.error(f"Error dismissing alert: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/monitoring/{user_id}/start")
async def start_monitoring(user_id: str, config: Optional[MonitoringConfig] = None):
    """Start monitoring for a user"""
    try:
        monitoring_config = config.dict() if config else None
        success = await event_integration_service.start_user_monitoring(user_id, monitoring_config)
        
        if success:
            return {"status": "success", "message": f"Monitoring started for user {user_id}"}
        else:
            raise HTTPException(status_code=500, detail="Failed to start monitoring")
            
    except Exception as e:
        logger.error(f"Error starting monitoring: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/monitoring/{user_id}/stop")
async def stop_monitoring(user_id: str):
    """Stop monitoring for a user"""
    try:
        success = await event_integration_service.stop_user_monitoring(user_id)
        
        if success:
            return {"status": "success", "message": f"Monitoring stopped for user {user_id}"}
        else:
            raise HTTPException(status_code=500, detail="Failed to stop monitoring")
            
    except Exception as e:
        logger.error(f"Error stopping monitoring: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/alert-preferences/{user_id}")
async def update_alert_preferences(user_id: str, preferences: AlertPreferences):
    """Update user alert preferences"""
    try:
        await alert_manager.update_user_preferences(user_id, preferences.dict())
        return {"status": "success", "message": "Alert preferences updated"}
        
    except Exception as e:
        logger.error(f"Error updating alert preferences: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time alerts and updates"""
    try:
        await connection_manager.connect(websocket, user_id)
        
        # Send welcome message
        await websocket.send_text(json.dumps({
            "type": "connection",
            "status": "connected",
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }))
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                if message.get('type') == 'ping':
                    await websocket.send_text(json.dumps({"type": "pong"}))
                elif message.get('type') == 'acknowledge_alert':
                    alert_id = message.get('alert_id')
                    if alert_id:
                        await alert_manager.acknowledge_alert(alert_id, user_id)
                        await websocket.send_text(json.dumps({
                            "type": "alert_acknowledged",
                            "alert_id": alert_id
                        }))
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Error handling WebSocket message from {user_id}: {str(e)}")
                
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {str(e)}")
    finally:
        connection_manager.disconnect(user_id)