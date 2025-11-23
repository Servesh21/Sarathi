from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class VehicleBase(BaseModel):
    vehicle_number: str
    vehicle_type: str
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None


class VehicleCreate(VehicleBase):
    pass


class VehicleResponse(VehicleBase):
    id: int
    user_id: int
    current_odometer_km: float = 0.0
    insurance_expiry: Optional[datetime] = None
    permit_expiry: Optional[datetime] = None
    fitness_expiry: Optional[datetime] = None
    puc_expiry: Optional[datetime] = None
    last_service_date: Optional[datetime] = None
    last_service_odometer: Optional[float] = None
    next_service_due_km: Optional[float] = None
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True


class VehicleUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    current_odometer_km: Optional[float] = None
    insurance_expiry: Optional[datetime] = None
    permit_expiry: Optional[datetime] = None
    fitness_expiry: Optional[datetime] = None
    puc_expiry: Optional[datetime] = None
    last_service_date: Optional[datetime] = None
    last_service_odometer: Optional[float] = None
    next_service_due_km: Optional[float] = None


class VehicleHealthCheckCreate(BaseModel):
    vehicle_id: int
    check_type: str = "image_diagnostic"
    odometer_reading: Optional[float] = None


class VehicleHealthCheckResponse(BaseModel):
    id: int
    vehicle_id: int
    check_type: str
    image_urls: Optional[List[str]] = None
    ai_analysis: Optional[str] = None
    detected_issues: Optional[List[Dict[str, Any]]] = None
    severity_score: Optional[float] = None
    tire_condition: Optional[str] = None
    engine_oil_level: Optional[str] = None
    brake_condition: Optional[str] = None
    battery_health: Optional[str] = None
    body_damage: Optional[str] = None
    immediate_action_required: bool = False
    recommendations: Optional[str] = None
    estimated_repair_cost: Optional[float] = None
    odometer_reading: Optional[float] = None
    status: str = "analyzed"
    created_at: datetime
    
    class Config:
        from_attributes = True


class VehicleHealthCheckUpdate(BaseModel):
    status: Optional[str] = None


class DiagnosticResult(BaseModel):
    overall_health: str
    severity_score: float
    detected_issues: List[Dict[str, Any]]
    recommendations: List[str]
    immediate_action_required: bool
    estimated_cost_range: Optional[str] = None
    next_check_in_days: int
