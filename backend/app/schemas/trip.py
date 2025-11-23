from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TripBase(BaseModel):
    start_location: str
    end_location: str
    start_lat: Optional[float] = None
    start_lng: Optional[float] = None
    end_lat: Optional[float] = None
    end_lng: Optional[float] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    distance_km: Optional[float] = None
    earnings: float
    fuel_cost: float = 0.0
    toll_cost: float = 0.0
    other_expenses: float = 0.0
    trip_type: str = "ride_hailing"
    platform: Optional[str] = None


class TripCreate(TripBase):
    pass


class TripVoiceCreate(BaseModel):
    voice_message_url: str
    transcription: Optional[str] = None


class TripResponse(TripBase):
    id: int
    user_id: int
    duration_minutes: Optional[float] = None
    net_earnings: Optional[float] = None
    is_high_value_zone: bool = False
    zone_rating: Optional[float] = None
    voice_message_url: Optional[str] = None
    transcription: Optional[str] = None
    status: str = "completed"
    profit_margin: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class TripUpdate(BaseModel):
    end_location: Optional[str] = None
    end_lat: Optional[float] = None
    end_lng: Optional[float] = None
    end_time: Optional[datetime] = None
    distance_km: Optional[float] = None
    earnings: Optional[float] = None
    fuel_cost: Optional[float] = None
    toll_cost: Optional[float] = None
    other_expenses: Optional[float] = None
    status: Optional[str] = None


class TripStats(BaseModel):
    total_trips: int
    total_earnings: float
    total_expenses: float
    net_earnings: float
    average_trip_earnings: float
    high_value_trips: int
    best_zone: Optional[str] = None
    best_time_slot: Optional[str] = None


class ZoneRecommendation(BaseModel):
    zone_name: str
    latitude: float
    longitude: float
    expected_earnings: float
    confidence_score: float
    reason: str
    best_time: str
