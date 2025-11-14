"""
Advanced SQLAlchemy database models for Sarathi AI Guardian application.
Includes models for knowledge management, predictive analytics, and resilience tracking.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum
from datetime import datetime
from typing import Dict, Any, Optional


# Enums for better type safety
class ResilienceLevel(enum.Enum):
    FRAGILE = "fragile"
    VULNERABLE = "vulnerable" 
    STABLE = "stable"
    RESILIENT = "resilient"
    ANTIFRAGILE = "antifragile"

class InterventionStatus(enum.Enum):
    PENDING = "pending"
    EXECUTED = "executed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class InterventionType(enum.Enum):
    EMERGENCY = "emergency"
    PREVENTIVE = "preventive"
    OPTIMIZATION = "optimization"
    GUIDANCE = "guidance"

class PredictionType(enum.Enum):
    VEHICLE_HEALTH = "vehicle_health"
    EARNINGS_FORECAST = "earnings_forecast"
    BURNOUT_RISK = "burnout_risk"
    FINANCIAL_RESILIENCE = "financial_resilience"


class User(Base):
    """Enhanced User model for driver accounts with comprehensive tracking"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    phone_number = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    
    # Driver profile information
    license_number = Column(String, unique=True)
    experience_years = Column(Float, default=0)
    preferred_areas = Column(JSON)  # List of preferred driving areas
    platforms_used = Column(JSON)  # List of platforms (Ola, Uber, etc.)
    
    # Current status tracking
    current_resilience_level = Column(Enum(ResilienceLevel), default=ResilienceLevel.STABLE)
    last_resilience_check = Column(DateTime(timezone=True))
    emergency_contact = Column(JSON)  # Emergency contact details
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    vehicles = relationship("Vehicle", back_populates="owner", cascade="all, delete-orphan")
    trips = relationship("Trip", back_populates="driver", cascade="all, delete-orphan")
    resilience_assessments = relationship("ResilienceAssessment", back_populates="user", cascade="all, delete-orphan")
    interventions = relationship("GuardianIntervention", back_populates="user", cascade="all, delete-orphan")
    predictions = relationship("PredictionRecord", back_populates="user", cascade="all, delete-orphan")
    knowledge_interactions = relationship("KnowledgeInteraction", back_populates="user", cascade="all, delete-orphan")
    financial_profiles = relationship("FinancialProfile", back_populates="user", cascade="all, delete-orphan")


class Vehicle(Base):
    """Enhanced Vehicle model with health tracking and maintenance history"""
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Basic vehicle info
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    license_plate = Column(String, unique=True, index=True)
    vehicle_type = Column(String, default="car")
    color = Column(String)
    vin_number = Column(String, unique=True)
    
    # Technical specifications
    fuel_efficiency = Column(Float)  # km per liter
    engine_capacity = Column(Float)  # in liters
    fuel_type = Column(String, default="petrol")  # petrol, diesel, cng, electric
    
    # Current status
    current_mileage = Column(Integer, default=0)
    last_service_date = Column(DateTime(timezone=True))
    last_service_mileage = Column(Integer, default=0)
    next_service_due = Column(DateTime(timezone=True))
    
    # Health tracking
    health_score = Column(Float, default=100.0)  # 0-100 health score
    maintenance_alerts = Column(JSON)  # Active maintenance alerts
    insurance_expiry = Column(DateTime(timezone=True))
    registration_expiry = Column(DateTime(timezone=True))
    
    # Financial
    purchase_price = Column(Float)
    current_market_value = Column(Float)
    monthly_emi = Column(Float, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="vehicles")
    trips = relationship("Trip", back_populates="vehicle", cascade="all, delete-orphan")
    maintenance_records = relationship("MaintenanceRecord", back_populates="vehicle", cascade="all, delete-orphan")


class Trip(Base):
    """Enhanced Trip model with comprehensive tracking"""
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    
    # Trip details
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    start_location = Column(JSON)  # {lat, lng, address}
    end_location = Column(JSON)    # {lat, lng, address}
    distance_km = Column(Float)
    duration_minutes = Column(Integer)
    
    # Financial details
    fare_amount = Column(Float)
    platform_commission = Column(Float)
    fuel_cost = Column(Float)
    toll_charges = Column(Float, default=0)
    net_earnings = Column(Float)
    platform_name = Column(String)  # ola, uber, rapido, etc.
    
    # Trip characteristics
    trip_type = Column(String)  # ride, delivery, long_distance
    passenger_rating = Column(Float)
    driver_rating = Column(Float)
    weather_conditions = Column(JSON)
    traffic_conditions = Column(String)
    
    # Advanced tracking
    route_efficiency = Column(Float)  # 0-1 scale
    earnings_per_km = Column(Float)
    earnings_per_hour = Column(Float)
    surge_multiplier = Column(Float, default=1.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    driver = relationship("User", back_populates="trips")
    vehicle = relationship("Vehicle", back_populates="trips")


class ResilienceAssessment(Base):
    """Track user resilience assessments over time"""
    __tablename__ = "resilience_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Overall scores
    overall_score = Column(Float, nullable=False)  # 0-100
    resilience_level = Column(Enum(ResilienceLevel), nullable=False)
    
    # Individual metric scores
    financial_stability = Column(Float)
    income_optimization = Column(Float)
    asset_protection = Column(Float)
    health_sustainability = Column(Float)
    growth_trajectory = Column(Float)
    risk_mitigation = Column(Float)
    
    # Context data
    assessment_context = Column(JSON)  # Input data used for assessment
    recommendations = Column(JSON)     # Generated recommendations
    confidence_score = Column(Float)   # Confidence in assessment
    
    # Metadata
    assessment_date = Column(DateTime(timezone=True), server_default=func.now())
    next_assessment_due = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="resilience_assessments")


class GuardianIntervention(Base):
    """Track autonomous guardian interventions"""
    __tablename__ = "guardian_interventions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Intervention details
    intervention_id = Column(String, unique=True, nullable=False)
    intervention_type = Column(Enum(InterventionType), nullable=False)
    urgency = Column(Integer)  # 1-4 priority level
    category = Column(String)  # financial, vehicle, health, earnings, growth
    
    # Content
    title = Column(String, nullable=False)
    description = Column(Text)
    immediate_actions = Column(JSON)  # List of immediate actions
    long_term_plan = Column(JSON)     # List of long-term actions
    
    # Execution details
    status = Column(Enum(InterventionStatus), default=InterventionStatus.PENDING)
    auto_executable = Column(Boolean, default=False)
    requires_confirmation = Column(Boolean, default=True)
    
    # Impact estimates
    expected_impact = Column(Text)
    cost_estimate = Column(Float, default=0)
    benefit_estimate = Column(Float, default=0)
    
    # Timing
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    scheduled_for = Column(DateTime(timezone=True))
    executed_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Results
    execution_results = Column(JSON)
    user_feedback = Column(JSON)
    effectiveness_score = Column(Float)  # 0-1 scale
    
    # Relationships
    user = relationship("User", back_populates="interventions")


class PredictionRecord(Base):
    """Store ML model predictions for analysis and improvement"""
    __tablename__ = "prediction_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Prediction details
    prediction_type = Column(Enum(PredictionType), nullable=False)
    model_version = Column(String)
    input_features = Column(JSON)  # Features used for prediction
    
    # Vehicle health predictions
    vehicle_health_score = Column(Float)
    failure_probability = Column(Float)
    maintenance_recommendations = Column(JSON)
    
    # Earnings predictions
    predicted_daily_earnings = Column(Float)
    optimal_hours = Column(JSON)
    location_recommendations = Column(JSON)
    
    # Burnout predictions
    burnout_risk_score = Column(Float)
    health_indicators = Column(JSON)
    rest_recommendations = Column(JSON)
    
    # Financial resilience predictions
    financial_resilience_score = Column(Float)
    investment_recommendations = Column(JSON)
    risk_factors = Column(JSON)
    
    # Metadata
    prediction_date = Column(DateTime(timezone=True), server_default=func.now())
    confidence_score = Column(Float)
    actual_outcome = Column(JSON)  # For measuring prediction accuracy
    accuracy_measured_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="predictions")


class KnowledgeInteraction(Base):
    """Track knowledge base interactions and learning"""
    __tablename__ = "knowledge_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Interaction details
    query = Column(Text, nullable=False)
    query_category = Column(String)  # earnings, vehicle, health, financial, regulatory
    
    # Knowledge retrieval results
    retrieved_knowledge = Column(JSON)  # RAG results
    knowledge_sources = Column(JSON)   # Sources used
    relevance_scores = Column(JSON)    # Relevance scores
    
    # Response details
    response_generated = Column(Text)
    response_quality = Column(Float)   # 0-1 scale
    user_satisfaction = Column(Float)  # 0-1 scale if provided
    
    # Learning data
    user_feedback = Column(JSON)
    follow_up_actions = Column(JSON)
    knowledge_gaps = Column(JSON)  # Identified gaps for improvement
    
    # Metadata
    interaction_date = Column(DateTime(timezone=True), server_default=func.now())
    session_id = Column(String)
    context_data = Column(JSON)  # User context during interaction
    
    # Relationships
    user = relationship("User", back_populates="knowledge_interactions")


class FinancialProfile(Base):
    """Comprehensive financial profile and wealth tracking"""
    __tablename__ = "financial_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Income tracking
    monthly_income_avg = Column(Float)
    monthly_income_variance = Column(Float)
    income_sources = Column(JSON)  # Multiple income sources
    
    # Expense tracking
    monthly_expenses_avg = Column(Float)
    expense_categories = Column(JSON)  # Categorized expenses
    fixed_expenses = Column(Float)
    variable_expenses = Column(Float)
    
    # Savings and emergency fund
    current_savings = Column(Float)
    emergency_fund = Column(Float)
    monthly_savings_target = Column(Float)
    savings_rate = Column(Float)  # Percentage of income saved
    
    # Investments
    investment_portfolio = Column(JSON)  # Different investment types
    total_invested = Column(Float)
    investment_returns = Column(Float)
    risk_tolerance = Column(String)  # low, medium, high
    
    # Debt obligations
    vehicle_loan = Column(Float, default=0)
    personal_loans = Column(Float, default=0)
    credit_card_debt = Column(Float, default=0)
    other_debts = Column(JSON)
    monthly_debt_payments = Column(Float, default=0)
    
    # Financial goals
    short_term_goals = Column(JSON)
    long_term_goals = Column(JSON)
    goal_progress = Column(JSON)
    
    # Insurance and protection
    health_insurance = Column(Boolean, default=False)
    vehicle_insurance_type = Column(String)  # third_party, comprehensive
    life_insurance = Column(Float, default=0)
    
    # Wealth metrics
    net_worth = Column(Float)
    financial_independence_score = Column(Float)  # 0-100
    wealth_building_rate = Column(Float)  # Monthly wealth increase
    
    # Risk assessment
    financial_risk_score = Column(Float)  # 0-100, lower is better
    income_stability_score = Column(Float)  # 0-100
    liquidity_score = Column(Float)  # 0-100
    
    # Metadata
    profile_updated_at = Column(DateTime(timezone=True), server_default=func.now())
    last_wealth_check = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="financial_profiles")


class MaintenanceRecord(Base):
    """Vehicle maintenance history and tracking"""
    __tablename__ = "maintenance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    
    # Maintenance details
    service_date = Column(DateTime(timezone=True), nullable=False)
    mileage_at_service = Column(Integer)
    service_type = Column(String)  # regular, emergency, warranty, inspection
    
    # Work performed
    services_performed = Column(JSON)  # List of services
    parts_replaced = Column(JSON)      # Parts replaced with costs
    issues_found = Column(JSON)        # Issues discovered
    issues_resolved = Column(JSON)     # Issues fixed
    
    # Financial details
    total_cost = Column(Float)
    labor_cost = Column(Float)
    parts_cost = Column(Float)
    service_provider = Column(String)  # Garage/service center name
    
    # Quality and outcome
    service_quality_rating = Column(Float)  # 1-5 stars
    post_service_health_score = Column(Float)  # Health score after service
    next_service_recommendation = Column(DateTime(timezone=True))
    
    # Predictive maintenance
    predicted_issues = Column(JSON)  # AI-predicted future issues
    preventive_recommendations = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="maintenance_records")


class MonitoringAlert(Base):
    """Real-time monitoring alerts and notifications"""
    __tablename__ = "monitoring_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Alert details
    alert_type = Column(String, nullable=False)  # vehicle, health, financial, earnings
    severity = Column(String)  # low, medium, high, critical
    title = Column(String, nullable=False)
    message = Column(Text)
    
    # Triggering conditions
    trigger_conditions = Column(JSON)
    threshold_values = Column(JSON)
    current_values = Column(JSON)
    
    # Alert status
    is_active = Column(Boolean, default=True)
    acknowledged = Column(Boolean, default=False)
    resolved = Column(Boolean, default=False)
    
    # Actions taken
    auto_actions_taken = Column(JSON)
    user_actions_required = Column(JSON)
    interventions_triggered = Column(JSON)
    
    # Timing
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    acknowledged_at = Column(DateTime(timezone=True))
    resolved_at = Column(DateTime(timezone=True))
    
    # Follow-up
    escalation_level = Column(Integer, default=0)
    next_check_due = Column(DateTime(timezone=True))


class LearningFeedback(Base):
    """Collect feedback for continuous learning and improvement"""
    __tablename__ = "learning_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Feedback context
    feedback_type = Column(String)  # prediction_accuracy, intervention_effectiveness, knowledge_quality
    related_id = Column(String)     # ID of related prediction/intervention/interaction
    
    # Feedback content
    user_rating = Column(Float)     # 1-5 stars
    feedback_text = Column(Text)
    satisfaction_score = Column(Float)  # 0-1 scale
    
    # Specific feedback
    prediction_accuracy = Column(Float)  # How accurate was the prediction?
    intervention_helpfulness = Column(Float)  # How helpful was the intervention?
    knowledge_relevance = Column(Float)   # How relevant was the knowledge?
    
    # Improvement suggestions
    improvement_suggestions = Column(JSON)
    feature_requests = Column(JSON)
    pain_points = Column(JSON)
    
    # Outcomes
    behavior_change = Column(Boolean)  # Did user change behavior based on guidance?
    outcome_achieved = Column(Boolean)  # Was the desired outcome achieved?
    outcome_description = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")


class SystemMetrics(Base):
    """Track system performance and analytics"""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Metric details
    metric_name = Column(String, nullable=False)
    metric_category = Column(String)  # prediction, intervention, knowledge, system
    metric_value = Column(Float)
    metric_unit = Column(String)
    
    # Context
    user_count = Column(Integer)
    time_period = Column(String)  # hourly, daily, weekly, monthly
    context_data = Column(JSON)
    
    # Performance indicators
    accuracy_score = Column(Float)
    response_time_ms = Column(Float)
    user_satisfaction = Column(Float)
    error_rate = Column(Float)
    
    # Aggregated data
    min_value = Column(Float)
    max_value = Column(Float)
    avg_value = Column(Float)
    std_deviation = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    date_bucket = Column(DateTime(timezone=True))  # For time-series analysis
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    start_location = Column(String, nullable=False)
    end_location = Column(String, nullable=False)
    distance_km = Column(Float, nullable=False)
    duration_minutes = Column(Integer)
    earnings = Column(Float, default=0.0)
    fuel_cost = Column(Float)
    trip_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    driver = relationship("User", back_populates="trips")
    vehicle = relationship("Vehicle", back_populates="trips")


class Conversation(Base):
    """Conversation model for storing agent chat history"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    query = Column(String, nullable=False)
    response = Column(String, nullable=False)
    agent_type = Column(String)  # earnings, resilience, general
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Goal(Base):
    """Goal model for user financial targets"""
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    deadline = Column(DateTime(timezone=True))
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
