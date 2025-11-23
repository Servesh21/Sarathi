from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Investment(Base):
    __tablename__ = "investments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Investment Details
    investment_name = Column(String(255), nullable=False)
    investment_type = Column(String(50), nullable=False)
    # Types: recurring_deposit, fixed_deposit, mutual_fund, gold, ppf, nps, etc.
    
    # Financial Details
    principal_amount = Column(Float, nullable=False)
    current_value = Column(Float, nullable=False)
    invested_amount = Column(Float, nullable=False)  # Total invested including contributions
    
    # Returns
    expected_return_rate = Column(Float, nullable=True)  # Annual percentage
    actual_return = Column(Float, default=0.0)
    
    # Timeline
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    maturity_date = Column(DateTime(timezone=True), nullable=True)
    
    # Recurring Investments
    is_recurring = Column(Boolean, default=False)
    recurring_amount = Column(Float, nullable=True)
    recurring_frequency = Column(String(20), nullable=True)  # monthly, quarterly, yearly
    
    # Risk Profile
    risk_level = Column(String(20), default="low")  # low, medium, high
    
    # Provider Details
    provider_name = Column(String(255), nullable=True)
    account_number = Column(String(100), nullable=True)
    
    # Status
    status = Column(String(20), default="active")  # active, matured, closed
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    matured_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="investments")
    
    @property
    def total_returns(self) -> float:
        """Calculate total returns"""
        return self.current_value - self.invested_amount
    
    @property
    def returns_percentage(self) -> float:
        """Calculate returns percentage"""
        if self.invested_amount > 0:
            return ((self.current_value - self.invested_amount) / self.invested_amount) * 100
        return 0.0


class InvestmentRecommendation(Base):
    __tablename__ = "investment_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Recommendation Details
    recommendation_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    
    # Financial Details
    suggested_amount = Column(Float, nullable=False)
    expected_return_rate = Column(Float, nullable=True)
    tenure_months = Column(Integer, nullable=True)
    risk_level = Column(String(20), default="low")
    
    # AI Analysis
    ai_reasoning = Column(Text, nullable=True)
    user_profile_match_score = Column(Float, nullable=True)  # 0-100
    
    # Market Data
    market_data = Column(JSON, nullable=True)
    
    # Action Status
    is_acted_upon = Column(Boolean, default=False)
    user_feedback = Column(String(20), nullable=True)  # interested, not_interested, completed
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    acted_upon_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User")
