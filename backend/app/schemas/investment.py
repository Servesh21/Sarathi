from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class InvestmentBase(BaseModel):
    investment_name: str
    investment_type: str
    principal_amount: float
    expected_return_rate: Optional[float] = None
    maturity_date: Optional[datetime] = None
    is_recurring: bool = False
    recurring_amount: Optional[float] = None
    recurring_frequency: Optional[str] = None
    risk_level: str = "low"
    provider_name: Optional[str] = None


class InvestmentCreate(InvestmentBase):
    pass


class InvestmentResponse(InvestmentBase):
    id: int
    user_id: int
    current_value: float
    invested_amount: float
    actual_return: float = 0.0
    start_date: datetime
    account_number: Optional[str] = None
    status: str = "active"
    total_returns: float
    returns_percentage: float
    created_at: datetime
    matured_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class InvestmentUpdate(BaseModel):
    current_value: Optional[float] = None
    invested_amount: Optional[float] = None
    maturity_date: Optional[datetime] = None
    status: Optional[str] = None
    recurring_amount: Optional[float] = None


class InvestmentRecommendationCreate(BaseModel):
    user_id: int
    recommendation_type: str
    title: str
    description: str
    suggested_amount: float
    expected_return_rate: Optional[float] = None
    tenure_months: Optional[int] = None
    risk_level: str = "low"
    ai_reasoning: Optional[str] = None
    market_data: Optional[Dict[str, Any]] = None


class InvestmentRecommendationResponse(BaseModel):
    id: int
    user_id: int
    recommendation_type: str
    title: str
    description: str
    suggested_amount: float
    expected_return_rate: Optional[float] = None
    tenure_months: Optional[int] = None
    risk_level: str
    ai_reasoning: Optional[str] = None
    user_profile_match_score: Optional[float] = None
    market_data: Optional[Dict[str, Any]] = None
    is_acted_upon: bool = False
    user_feedback: Optional[str] = None
    created_at: datetime
    expires_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class InvestmentRecommendationUpdate(BaseModel):
    is_acted_upon: Optional[bool] = None
    user_feedback: Optional[str] = None


class PortfolioSummary(BaseModel):
    total_invested: float
    current_portfolio_value: float
    total_returns: float
    returns_percentage: float
    active_investments: int
    monthly_recurring_total: float
    investment_breakdown: Dict[str, float]
    risk_distribution: Dict[str, float]


class SurplusAnalysis(BaseModel):
    monthly_income: float
    monthly_expenses: float
    monthly_surplus: float
    surplus_percentage: float
    recommended_savings: float
    recommended_investments: float
    emergency_fund_status: str
    insights: List[str]
