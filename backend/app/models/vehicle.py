from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Vehicle Information
    vehicle_number = Column(String(20), unique=True, index=True, nullable=False)
    vehicle_type = Column(String(50), nullable=False)  # auto, bike, car
    make = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    year = Column(Integer, nullable=True)
    
    # Odometer
    current_odometer_km = Column(Float, default=0.0)
    
    # Insurance & Documents
    insurance_expiry = Column(DateTime(timezone=True), nullable=True)
    permit_expiry = Column(DateTime(timezone=True), nullable=True)
    fitness_expiry = Column(DateTime(timezone=True), nullable=True)
    puc_expiry = Column(DateTime(timezone=True), nullable=True)
    
    # Maintenance Schedule
    last_service_date = Column(DateTime(timezone=True), nullable=True)
    last_service_odometer = Column(Float, nullable=True)
    next_service_due_km = Column(Float, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="vehicles")
    health_checks = relationship("VehicleHealthCheck", back_populates="vehicle", cascade="all, delete-orphan")


class VehicleHealthCheck(Base):
    __tablename__ = "vehicle_health_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    
    # Check Type
    check_type = Column(String(50), nullable=False)  # routine, image_diagnostic, emergency
    
    # Image Upload
    image_urls = Column(JSON, nullable=True)  # List of uploaded image URLs
    
    # AI Diagnostic Results
    ai_analysis = Column(Text, nullable=True)
    detected_issues = Column(JSON, nullable=True)  # List of detected issues
    severity_score = Column(Float, nullable=True)  # 0-100 scale
    
    # Component Health
    tire_condition = Column(String(20), nullable=True)  # good, fair, poor, critical
    engine_oil_level = Column(String(20), nullable=True)
    brake_condition = Column(String(20), nullable=True)
    battery_health = Column(String(20), nullable=True)
    body_damage = Column(String(20), nullable=True)
    
    # Recommendations
    immediate_action_required = Column(Boolean, default=False)
    recommendations = Column(Text, nullable=True)
    estimated_repair_cost = Column(Float, nullable=True)
    
    # Odometer at check
    odometer_reading = Column(Float, nullable=True)
    
    # Status
    status = Column(String(20), default="analyzed")  # pending, analyzed, action_taken
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="health_checks")
