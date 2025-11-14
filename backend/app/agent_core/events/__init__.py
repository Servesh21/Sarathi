"""
Event-Driven Architecture Module for Sarathi Guardian System
Provides real-time monitoring, event processing, and alert management
"""

from .realtime_system import (
    EventType,
    EventSeverity,
    SarathiEvent,
    EventProcessor,
    RealTimeMonitor,
    event_processor,
    realtime_monitor
)

from .alert_system import (
    AlertChannel,
    AlertPriority,
    AlertStatus,
    SarathiAlert,
    AlertManager,
    EmergencyNotificationSystem,
    alert_manager,
    emergency_system
)

from .integration import (
    EventIntegrationService,
    WebSocketConnectionManager,
    event_integration_service,
    connection_manager,
    router as events_router
)

# Initialize the event system
async def initialize_event_system():
    """Initialize the complete event-driven system"""
    await event_integration_service.initialize()

# Export main interfaces
__all__ = [
    # Event types and enums
    'EventType',
    'EventSeverity', 
    'AlertChannel',
    'AlertPriority',
    'AlertStatus',
    
    # Data models
    'SarathiEvent',
    'SarathiAlert',
    
    # Services
    'EventProcessor',
    'RealTimeMonitor', 
    'AlertManager',
    'EmergencyNotificationSystem',
    'EventIntegrationService',
    'WebSocketConnectionManager',
    
    # Global instances
    'event_processor',
    'realtime_monitor',
    'alert_manager',
    'emergency_system',
    'event_integration_service',
    'connection_manager',
    'events_router',
    
    # Initialization
    'initialize_event_system'
]