from app.schemas.user import UserCreate, UserResponse, UserLogin, UserUpdate, Token
from app.schemas.trip import (
    TripCreate, TripResponse, TripUpdate, TripVoiceCreate, 
    TripStats, ZoneRecommendation
)
from app.schemas.vehicle import (
    VehicleCreate, VehicleResponse, VehicleUpdate,
    VehicleHealthCheckCreate, VehicleHealthCheckResponse, 
    VehicleHealthCheckUpdate, DiagnosticResult
)
from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdate, AlertStats
from app.schemas.goal import (
    GoalCreate, GoalResponse, GoalUpdate,
    GoalProgressCreate, GoalProgressResponse, GoalInsights
)
from app.schemas.investment import (
    InvestmentCreate, InvestmentResponse, InvestmentUpdate,
    InvestmentRecommendationCreate, InvestmentRecommendationResponse,
    InvestmentRecommendationUpdate, PortfolioSummary, SurplusAnalysis
)

__all__ = [
    "UserCreate", "UserResponse", "UserLogin", "UserUpdate", "Token",
    "TripCreate", "TripResponse", "TripUpdate", "TripVoiceCreate", "TripStats", "ZoneRecommendation",
    "VehicleCreate", "VehicleResponse", "VehicleUpdate",
    "VehicleHealthCheckCreate", "VehicleHealthCheckResponse", "VehicleHealthCheckUpdate", "DiagnosticResult",
    "AlertCreate", "AlertResponse", "AlertUpdate", "AlertStats",
    "GoalCreate", "GoalResponse", "GoalUpdate", "GoalProgressCreate", "GoalProgressResponse", "GoalInsights",
    "InvestmentCreate", "InvestmentResponse", "InvestmentUpdate",
    "InvestmentRecommendationCreate", "InvestmentRecommendationResponse",
    "InvestmentRecommendationUpdate", "PortfolioSummary", "SurplusAnalysis"
]
