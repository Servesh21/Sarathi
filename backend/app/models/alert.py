from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Alert Type
    alert_type = Column(String(50), nullable=False)
    # Types: vehicle_maintenance, document_expiry, fatigue_warning, 
    #        earnings_drop, high_expense, goal_reminder, investment_opportunity
    
    # Alert Priority
    priority = Column(String(20), default="medium")  # low, medium, high, critical
    
    # Content
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    
    # Action Required
    action_required = Column(Boolean, default=False)
    action_type = Column(String(50), nullable=True)  # book_service, renew_document, rest, etc.
    action_url = Column(String(500), nullable=True)
    
    # Metadata
    alert_metadata = Column(JSON, nullable=True)  # Additional context data
    
    # Delivery Status
    is_read = Column(Boolean, default=False)
    sent_to_whatsapp = Column(Boolean, default=False)
    whatsapp_sent_at = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    status = Column(String(20), default="active")  # active, dismissed, resolved
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="alerts")
