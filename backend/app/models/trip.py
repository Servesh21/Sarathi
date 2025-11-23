from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Trip Details
    start_location = Column(String(255), nullable=False)
    end_location = Column(String(255), nullable=False)
    start_lat = Column(Float, nullable=True)
    start_lng = Column(Float, nullable=True)
    end_lat = Column(Float, nullable=True)
    end_lng = Column(Float, nullable=True)
    
    # Timing
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    duration_minutes = Column(Float, nullable=True)
    
    # Financial
    distance_km = Column(Float, nullable=True)
    earnings = Column(Float, nullable=False)
    fuel_cost = Column(Float, default=0.0)
    toll_cost = Column(Float, default=0.0)
    other_expenses = Column(Float, default=0.0)
    net_earnings = Column(Float, nullable=True)
    
    # Trip Type
    trip_type = Column(String(50), default="ride_hailing")  # ride_hailing, delivery, other
    platform = Column(String(50), nullable=True)  # uber, ola, swiggy, zomato, etc.
    
    # AI Analysis
    is_high_value_zone = Column(Boolean, default=False)
    zone_rating = Column(Float, nullable=True)  # AI-computed zone quality score
    
    # Voice Input
    voice_message_url = Column(String(500), nullable=True)
    transcription = Column(Text, nullable=True)
    
    # Status
    status = Column(String(20), default="completed")  # completed, cancelled, ongoing
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="trips")
    
    @property
    def profit_margin(self) -> float:
        """Calculate profit margin percentage"""
        if self.earnings > 0:
            total_cost = self.fuel_cost + self.toll_cost + self.other_expenses
            return ((self.earnings - total_cost) / self.earnings) * 100
        return 0.0
