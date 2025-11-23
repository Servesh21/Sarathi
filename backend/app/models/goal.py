from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Goal Details
    goal_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    goal_type = Column(String(50), default="savings")  # savings, asset_purchase, emergency_fund
    
    # Financial Target
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    monthly_contribution = Column(Float, default=0.0)
    
    # Timeline
    target_date = Column(DateTime(timezone=True), nullable=True)
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status
    status = Column(String(20), default="in_progress")  # in_progress, completed, paused, cancelled
    completion_percentage = Column(Float, default=0.0)
    
    # AI Recommendations
    suggested_monthly_savings = Column(Float, nullable=True)
    recommended_adjustments = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="goals")
    progress_history = relationship("GoalProgress", back_populates="goal", cascade="all, delete-orphan")
    
    @property
    def percentage_complete(self) -> float:
        """Calculate completion percentage"""
        if self.target_amount > 0:
            return min((self.current_amount / self.target_amount) * 100, 100.0)
        return 0.0


class GoalProgress(Base):
    __tablename__ = "goal_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="CASCADE"), nullable=False)
    
    # Progress Entry
    amount_added = Column(Float, nullable=False)
    previous_total = Column(Float, nullable=False)
    new_total = Column(Float, nullable=False)
    
    # Notes
    notes = Column(Text, nullable=True)
    source = Column(String(100), nullable=True)  # savings, bonus, side_income, etc.
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    goal = relationship("Goal", back_populates="progress_history")
