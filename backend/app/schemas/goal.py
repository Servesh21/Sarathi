from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GoalBase(BaseModel):
    goal_name: str
    description: Optional[str] = None
    goal_type: str = "savings"
    target_amount: float
    monthly_contribution: float = 0.0
    target_date: Optional[datetime] = None


class GoalCreate(GoalBase):
    pass


class GoalResponse(GoalBase):
    id: int
    user_id: int
    current_amount: float = 0.0
    start_date: datetime
    status: str = "in_progress"
    completion_percentage: float = 0.0
    percentage_complete: float
    suggested_monthly_savings: Optional[float] = None
    recommended_adjustments: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class GoalUpdate(BaseModel):
    goal_name: Optional[str] = None
    description: Optional[str] = None
    target_amount: Optional[float] = None
    monthly_contribution: Optional[float] = None
    target_date: Optional[datetime] = None
    status: Optional[str] = None


class GoalProgressCreate(BaseModel):
    goal_id: int
    amount_added: float
    notes: Optional[str] = None
    source: Optional[str] = None


class GoalProgressResponse(BaseModel):
    id: int
    goal_id: int
    amount_added: float
    previous_total: float
    new_total: float
    notes: Optional[str] = None
    source: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class GoalInsights(BaseModel):
    goal_id: int
    goal_name: str
    days_to_target: int
    required_monthly_savings: float
    current_pace: str  # on_track, ahead, behind
    projected_completion_date: Optional[datetime] = None
    recommendations: List[str]
