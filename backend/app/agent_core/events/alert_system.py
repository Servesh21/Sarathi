"""
Alert Management System for Sarathi Guardian
Handles push notifications, in-app alerts, and emergency communications
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from pydantic import BaseModel, Field

# Internal imports
from .realtime_system import SarathiEvent, EventType, EventSeverity

logger = logging.getLogger(__name__)

class AlertChannel(Enum):
    """Available alert channels"""
    PUSH_NOTIFICATION = "push_notification"
    IN_APP = "in_app"
    SMS = "sms"
    VOICE_CALL = "voice_call"
    EMAIL = "email"
    EMERGENCY_CONTACT = "emergency_contact"

class AlertPriority(Enum):
    """Alert priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5

class AlertStatus(Enum):
    """Alert status tracking"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    ACKNOWLEDGED = "acknowledged"
    DISMISSED = "dismissed"
    FAILED = "failed"

@dataclass
class SarathiAlert:
    """Sarathi alert structure"""
    alert_id: str
    user_id: str
    title: str
    message: str
    priority: AlertPriority
    channels: List[AlertChannel]
    source_event: Optional[str] = None  # Source event ID
    data: Dict[str, Any] = None
    actions: List[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None
    created_at: datetime = None
    status: AlertStatus = AlertStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3

    def __post_init__(self):
        if self.data is None:
            self.data = {}
        if self.actions is None:
            self.actions = []
        if self.created_at is None:
            self.created_at = datetime.now()

class AlertManager:
    """Central alert management system"""
    
    def __init__(self):
        self.pending_alerts: Dict[str, SarathiAlert] = {}
        self.sent_alerts: Dict[str, SarathiAlert] = {}
        self.alert_templates = {}
        self.user_preferences: Dict[str, Dict] = {}
        
        # Channel handlers
        self.channel_handlers = {
            AlertChannel.PUSH_NOTIFICATION: self._send_push_notification,
            AlertChannel.IN_APP: self._send_in_app_alert,
            AlertChannel.SMS: self._send_sms,
            AlertChannel.VOICE_CALL: self._make_voice_call,
            AlertChannel.EMAIL: self._send_email,
            AlertChannel.EMERGENCY_CONTACT: self._alert_emergency_contact
        }
        
        # Initialize alert templates
        self._initialize_alert_templates()
        
        logger.info("Alert Manager initialized")
    
    async def create_alert_from_event(self, event: SarathiEvent) -> Optional[SarathiAlert]:
        """Create an alert from a Sarathi event"""
        try:
            # Get alert configuration for this event type
            alert_config = self._get_alert_config_for_event(event)
            
            if not alert_config:
                return None
            
            # Create alert
            alert = SarathiAlert(
                alert_id=str(uuid.uuid4()),
                user_id=event.user_id,
                title=alert_config['title'],
                message=alert_config['message'].format(**event.data),
                priority=self._get_priority_for_severity(event.severity),
                channels=alert_config['channels'],
                source_event=event.event_id,
                data=event.data,
                actions=alert_config.get('actions', []),
                expires_at=alert_config.get('expires_at')
            )
            
            # Apply user preferences
            alert = await self._apply_user_preferences(alert)
            
            return alert
            
        except Exception as e:
            logger.error(f"Error creating alert from event: {str(e)}")
            return None
    
    async def send_alert(self, alert: SarathiAlert) -> bool:
        """Send an alert through configured channels"""
        try:
            self.pending_alerts[alert.alert_id] = alert
            
            # Send through each channel
            success_count = 0
            for channel in alert.channels:
                try:
                    handler = self.channel_handlers.get(channel)
                    if handler:
                        success = await handler(alert)
                        if success:
                            success_count += 1
                    else:
                        logger.warning(f"No handler for channel: {channel}")
                except Exception as channel_error:
                    logger.error(f"Error sending alert via {channel}: {str(channel_error)}")
            
            # Update alert status
            if success_count > 0:
                alert.status = AlertStatus.SENT
                self.sent_alerts[alert.alert_id] = alert
                if alert.alert_id in self.pending_alerts:
                    del self.pending_alerts[alert.alert_id]
                
                logger.info(f"Alert sent successfully: {alert.alert_id} ({success_count}/{len(alert.channels)} channels)")
                return True
            else:
                alert.status = AlertStatus.FAILED
                alert.retry_count += 1
                
                # Retry if under limit
                if alert.retry_count < alert.max_retries:
                    await asyncio.sleep(30)  # Wait before retry
                    return await self.send_alert(alert)
                
                logger.error(f"Alert failed to send: {alert.alert_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending alert: {str(e)}")
            return False
    
    async def send_immediate_alert(self, user_id: str, title: str, message: str, 
                                 priority: AlertPriority = AlertPriority.HIGH,
                                 channels: List[AlertChannel] = None,
                                 actions: List[Dict] = None) -> bool:
        """Send an immediate alert"""
        try:
            if channels is None:
                channels = [AlertChannel.PUSH_NOTIFICATION, AlertChannel.IN_APP]
            
            alert = SarathiAlert(
                alert_id=str(uuid.uuid4()),
                user_id=user_id,
                title=title,
                message=message,
                priority=priority,
                channels=channels,
                actions=actions or []
            )
            
            return await self.send_alert(alert)
            
        except Exception as e:
            logger.error(f"Error sending immediate alert: {str(e)}")
            return False
    
    async def acknowledge_alert(self, alert_id: str, user_id: str) -> bool:
        """Acknowledge an alert"""
        try:
            alert = self.sent_alerts.get(alert_id)
            if alert and alert.user_id == user_id:
                alert.status = AlertStatus.ACKNOWLEDGED
                logger.info(f"Alert acknowledged: {alert_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error acknowledging alert: {str(e)}")
            return False
    
    async def dismiss_alert(self, alert_id: str, user_id: str) -> bool:
        """Dismiss an alert"""
        try:
            alert = self.sent_alerts.get(alert_id)
            if alert and alert.user_id == user_id:
                alert.status = AlertStatus.DISMISSED
                logger.info(f"Alert dismissed: {alert_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error dismissing alert: {str(e)}")
            return False
    
    async def get_user_alerts(self, user_id: str, status: Optional[AlertStatus] = None,
                            limit: int = 50) -> List[SarathiAlert]:
        """Get alerts for a user"""
        try:
            alerts = []
            
            # Check both pending and sent alerts
            all_alerts = {**self.pending_alerts, **self.sent_alerts}
            
            for alert in all_alerts.values():
                if alert.user_id == user_id:
                    if status is None or alert.status == status:
                        alerts.append(alert)
            
            # Sort by creation time (newest first)
            alerts.sort(key=lambda x: x.created_at, reverse=True)
            
            return alerts[:limit]
            
        except Exception as e:
            logger.error(f"Error getting user alerts: {str(e)}")
            return []
    
    def _initialize_alert_templates(self):
        """Initialize alert templates for different event types"""
        self.alert_templates = {
            EventType.VEHICLE_CRITICAL: {
                'title': '🚨 Critical Vehicle Alert',
                'message': 'Your vehicle needs immediate attention: {issue_description}',
                'channels': [AlertChannel.PUSH_NOTIFICATION, AlertChannel.IN_APP, AlertChannel.SMS],
                'actions': [
                    {'type': 'find_service_center', 'label': 'Find Service Center'},
                    {'type': 'call_emergency', 'label': 'Call Emergency Service'}
                ]
            },
            EventType.VEHICLE_WARNING: {
                'title': '⚠️ Vehicle Maintenance Alert',
                'message': 'Vehicle maintenance required: {warning_description}',
                'channels': [AlertChannel.PUSH_NOTIFICATION, AlertChannel.IN_APP],
                'actions': [
                    {'type': 'schedule_maintenance', 'label': 'Schedule Maintenance'},
                    {'type': 'view_details', 'label': 'View Details'}
                ]
            },
            EventType.HEALTH_EMERGENCY: {
                'title': '🏥 Health Emergency Alert',
                'message': 'Health concern detected. Please take rest immediately.',
                'channels': [AlertChannel.PUSH_NOTIFICATION, AlertChannel.IN_APP, AlertChannel.EMERGENCY_CONTACT],
                'actions': [
                    {'type': 'start_rest_mode', 'label': 'Start Rest Mode'},
                    {'type': 'contact_doctor', 'label': 'Contact Doctor'}
                ]
            },
            EventType.BURNOUT_WARNING: {
                'title': '😴 Rest Recommendation',
                'message': 'You may be experiencing burnout. Consider taking a break.',
                'channels': [AlertChannel.PUSH_NOTIFICATION, AlertChannel.IN_APP],
                'actions': [
                    {'type': 'schedule_rest', 'label': 'Schedule Rest Day'},
                    {'type': 'view_wellness_tips', 'label': 'Wellness Tips'}
                ]
            },
            EventType.FINANCIAL_CRISIS: {
                'title': '💰 Financial Alert',
                'message': 'Low emergency funds detected. Immediate action recommended.',
                'channels': [AlertChannel.PUSH_NOTIFICATION, AlertChannel.IN_APP],
                'actions': [
                    {'type': 'view_opportunities', 'label': 'Find Income Opportunities'},
                    {'type': 'emergency_mode', 'label': 'Enable Emergency Mode'}
                ]
            },
            EventType.EARNINGS_DROP: {
                'title': '📉 Earnings Alert',
                'message': 'Earnings below average. Optimization suggestions available.',
                'channels': [AlertChannel.PUSH_NOTIFICATION, AlertChannel.IN_APP],
                'actions': [
                    {'type': 'view_optimization', 'label': 'View Optimization Tips'},
                    {'type': 'check_opportunities', 'label': 'Find Opportunities'}
                ]
            },
            EventType.SURGE_DETECTED: {
                'title': '🚀 Surge Alert',
                'message': 'High demand detected in {area}! Multiplier: {multiplier}x',
                'channels': [AlertChannel.PUSH_NOTIFICATION],
                'actions': [
                    {'type': 'navigate_to_area', 'label': 'Navigate'},
                    {'type': 'view_map', 'label': 'View on Map'}
                ],
                'expires_at': lambda: datetime.now() + timedelta(minutes=30)
            },
            EventType.HIGH_DEMAND: {
                'title': '📈 High Demand Alert',
                'message': 'High demand period detected. Potential earnings increase: {potential_increase}',
                'channels': [AlertChannel.PUSH_NOTIFICATION],
                'actions': [
                    {'type': 'view_hotspots', 'label': 'View Hotspots'},
                    {'type': 'optimize_route', 'label': 'Optimize Route'}
                ]
            },
            EventType.WEATHER_OPPORTUNITY: {
                'title': '🌧️ Weather Opportunity',
                'message': 'Weather conditions may increase demand. Position strategically.',
                'channels': [AlertChannel.PUSH_NOTIFICATION],
                'actions': [
                    {'type': 'view_strategy', 'label': 'View Strategy'},
                    {'type': 'check_weather', 'label': 'Weather Details'}
                ]
            },
            EventType.MAINTENANCE_DUE: {
                'title': '🔧 Maintenance Due',
                'message': 'Vehicle maintenance is due. Schedule soon to avoid issues.',
                'channels': [AlertChannel.IN_APP],
                'actions': [
                    {'type': 'schedule_maintenance', 'label': 'Schedule Now'},
                    {'type': 'find_service_center', 'label': 'Find Service Center'}
                ]
            },
            EventType.SAFETY_ALERT: {
                'title': '⚡ Safety Alert',
                'message': 'Safety concern detected. Please review immediately.',
                'channels': [AlertChannel.PUSH_NOTIFICATION, AlertChannel.IN_APP],
                'actions': [
                    {'type': 'view_details', 'label': 'View Details'},
                    {'type': 'contact_support', 'label': 'Contact Support'}
                ]
            }
        }
    
    def _get_alert_config_for_event(self, event: SarathiEvent) -> Optional[Dict]:
        """Get alert configuration for an event type"""
        template = self.alert_templates.get(event.event_type)
        
        if not template:
            return None
        
        config = template.copy()
        
        # Handle dynamic expires_at
        if 'expires_at' in config and callable(config['expires_at']):
            config['expires_at'] = config['expires_at']()
        
        return config
    
    def _get_priority_for_severity(self, severity: EventSeverity) -> AlertPriority:
        """Map event severity to alert priority"""
        mapping = {
            EventSeverity.LOW: AlertPriority.LOW,
            EventSeverity.MEDIUM: AlertPriority.NORMAL,
            EventSeverity.HIGH: AlertPriority.HIGH,
            EventSeverity.CRITICAL: AlertPriority.EMERGENCY
        }
        return mapping.get(severity, AlertPriority.NORMAL)
    
    async def _apply_user_preferences(self, alert: SarathiAlert) -> SarathiAlert:
        """Apply user preferences to alert"""
        try:
            preferences = self.user_preferences.get(alert.user_id, {})
            
            # Filter channels based on preferences
            if 'disabled_channels' in preferences:
                disabled = set(preferences['disabled_channels'])
                alert.channels = [ch for ch in alert.channels if ch not in disabled]
            
            # Apply quiet hours
            if 'quiet_hours' in preferences:
                quiet_hours = preferences['quiet_hours']
                current_hour = datetime.now().hour
                
                if quiet_hours['start'] <= current_hour <= quiet_hours['end']:
                    # During quiet hours, only send critical alerts
                    if alert.priority < AlertPriority.CRITICAL:
                        # Remove sound-based channels
                        alert.channels = [ch for ch in alert.channels 
                                        if ch not in [AlertChannel.SMS, AlertChannel.VOICE_CALL]]
            
            return alert
            
        except Exception as e:
            logger.error(f"Error applying user preferences: {str(e)}")
            return alert
    
    # Channel handler methods
    async def _send_push_notification(self, alert: SarathiAlert) -> bool:
        """Send push notification"""
        try:
            # This would integrate with Firebase/Apple Push Notification Service
            # For now, log the notification
            logger.info(f"PUSH: {alert.title} -> {alert.user_id}")
            logger.info(f"MESSAGE: {alert.message}")
            
            # Simulate success/failure
            return True
            
        except Exception as e:
            logger.error(f"Error sending push notification: {str(e)}")
            return False
    
    async def _send_in_app_alert(self, alert: SarathiAlert) -> bool:
        """Send in-app alert"""
        try:
            # This would send to WebSocket or store in database for app to fetch
            logger.info(f"IN-APP: {alert.title} -> {alert.user_id}")
            
            # Store alert for app to fetch
            # In production, this would be stored in database or sent via WebSocket
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending in-app alert: {str(e)}")
            return False
    
    async def _send_sms(self, alert: SarathiAlert) -> bool:
        """Send SMS alert"""
        try:
            # This would integrate with SMS service (Twilio, AWS SNS, etc.)
            logger.info(f"SMS: {alert.message} -> {alert.user_id}")
            
            # Only send SMS for high priority alerts
            if alert.priority >= AlertPriority.HIGH:
                # Simulate SMS sending
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error sending SMS: {str(e)}")
            return False
    
    async def _make_voice_call(self, alert: SarathiAlert) -> bool:
        """Make voice call alert"""
        try:
            # This would integrate with voice calling service
            logger.critical(f"VOICE CALL: {alert.message} -> {alert.user_id}")
            
            # Only make voice calls for emergency alerts
            if alert.priority == AlertPriority.EMERGENCY:
                # Simulate voice call
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error making voice call: {str(e)}")
            return False
    
    async def _send_email(self, alert: SarathiAlert) -> bool:
        """Send email alert"""
        try:
            # This would integrate with email service
            logger.info(f"EMAIL: {alert.title} -> {alert.user_id}")
            
            # Email for non-urgent but important alerts
            if alert.priority >= AlertPriority.NORMAL:
                # Simulate email sending
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    async def _alert_emergency_contact(self, alert: SarathiAlert) -> bool:
        """Alert emergency contact"""
        try:
            # This would contact the user's emergency contact
            logger.critical(f"EMERGENCY CONTACT ALERT: {alert.message} -> {alert.user_id}")
            
            # Only for health emergencies and critical situations
            if alert.priority == AlertPriority.EMERGENCY and alert.source_event:
                # Get emergency contact from user data
                # Send notification to emergency contact
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error alerting emergency contact: {str(e)}")
            return False
    
    async def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Update user alert preferences"""
        try:
            self.user_preferences[user_id] = preferences
            logger.info(f"Alert preferences updated for user {user_id}")
        except Exception as e:
            logger.error(f"Error updating user preferences: {str(e)}")


class EmergencyNotificationSystem:
    """Emergency notification system with escalation"""
    
    def __init__(self, alert_manager: AlertManager):
        self.alert_manager = alert_manager
        self.escalation_rules = {}
        self._setup_escalation_rules()
    
    def _setup_escalation_rules(self):
        """Setup escalation rules for different emergency types"""
        self.escalation_rules = {
            'health_emergency': {
                'initial_channels': [AlertChannel.PUSH_NOTIFICATION, AlertChannel.IN_APP],
                'escalation_delay_minutes': 5,
                'escalation_channels': [AlertChannel.SMS, AlertChannel.VOICE_CALL],
                'final_escalation_channels': [AlertChannel.EMERGENCY_CONTACT]
            },
            'vehicle_critical': {
                'initial_channels': [AlertChannel.PUSH_NOTIFICATION, AlertChannel.SMS],
                'escalation_delay_minutes': 10,
                'escalation_channels': [AlertChannel.VOICE_CALL],
                'final_escalation_channels': []
            },
            'financial_crisis': {
                'initial_channels': [AlertChannel.PUSH_NOTIFICATION, AlertChannel.IN_APP],
                'escalation_delay_minutes': 30,
                'escalation_channels': [AlertChannel.SMS],
                'final_escalation_channels': []
            }
        }
    
    async def send_emergency_alert(self, user_id: str, emergency_type: str, 
                                 title: str, message: str, context: Dict[str, Any] = None):
        """Send emergency alert with escalation"""
        try:
            rules = self.escalation_rules.get(emergency_type)
            if not rules:
                # Default emergency handling
                return await self.alert_manager.send_immediate_alert(
                    user_id, title, message, AlertPriority.EMERGENCY
                )
            
            # Send initial alert
            initial_alert = SarathiAlert(
                alert_id=str(uuid.uuid4()),
                user_id=user_id,
                title=title,
                message=message,
                priority=AlertPriority.EMERGENCY,
                channels=rules['initial_channels'],
                data=context or {}
            )
            
            success = await self.alert_manager.send_alert(initial_alert)
            
            if success:
                # Schedule escalation
                await self._schedule_escalation(initial_alert, rules)
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending emergency alert: {str(e)}")
            return False
    
    async def _schedule_escalation(self, original_alert: SarathiAlert, rules: Dict):
        """Schedule alert escalation"""
        try:
            escalation_delay = rules['escalation_delay_minutes'] * 60  # Convert to seconds
            
            # Wait for escalation delay
            await asyncio.sleep(escalation_delay)
            
            # Check if alert was acknowledged
            current_alert = self.alert_manager.sent_alerts.get(original_alert.alert_id)
            if not current_alert or current_alert.status in [AlertStatus.ACKNOWLEDGED, AlertStatus.DISMISSED]:
                logger.info(f"Alert {original_alert.alert_id} was acknowledged, skipping escalation")
                return
            
            # Send escalation alert
            escalation_alert = SarathiAlert(
                alert_id=str(uuid.uuid4()),
                user_id=original_alert.user_id,
                title=f"ESCALATED: {original_alert.title}",
                message=f"Previous alert not acknowledged. {original_alert.message}",
                priority=AlertPriority.EMERGENCY,
                channels=rules['escalation_channels'],
                data=original_alert.data,
                source_event=original_alert.source_event
            )
            
            escalation_success = await self.alert_manager.send_alert(escalation_alert)
            
            if escalation_success and rules.get('final_escalation_channels'):
                # Schedule final escalation
                await asyncio.sleep(escalation_delay)
                
                # Check again if acknowledged
                if escalation_alert.status not in [AlertStatus.ACKNOWLEDGED, AlertStatus.DISMISSED]:
                    final_alert = SarathiAlert(
                        alert_id=str(uuid.uuid4()),
                        user_id=original_alert.user_id,
                        title=f"FINAL ESCALATION: {original_alert.title}",
                        message=f"Emergency situation requires immediate attention. {original_alert.message}",
                        priority=AlertPriority.EMERGENCY,
                        channels=rules['final_escalation_channels'],
                        data=original_alert.data,
                        source_event=original_alert.source_event
                    )
                    
                    await self.alert_manager.send_alert(final_alert)
            
        except Exception as e:
            logger.error(f"Error in escalation: {str(e)}")


# Global instances
alert_manager = AlertManager()
emergency_system = EmergencyNotificationSystem(alert_manager)