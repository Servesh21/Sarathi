from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class AlertBase(BaseModel):
    alert_type: str
    title: str
    message: str
    priority: str = "medium"
    action_required: bool = False
    action_type: Optional[str] = None
    action_url: Optional[str] = None


class AlertCreate(AlertBase):
    user_id: int
    alert_metadata: Optional[Dict[str, Any]] = None


class AlertResponse(AlertBase):
    id: int
    user_id: int
    alert_metadata: Optional[Dict[str, Any]] = None
    is_read: bool = False
    sent_to_whatsapp: bool = False
    whatsapp_sent_at: Optional[datetime] = None
    status: str = "active"
    resolved_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class AlertUpdate(BaseModel):
    is_read: Optional[bool] = None
    status: Optional[str] = None


class AlertStats(BaseModel):
    total_alerts: int
    unread_alerts: int
    critical_alerts: int
    active_alerts: int
    alerts_by_type: Dict[str, int]
