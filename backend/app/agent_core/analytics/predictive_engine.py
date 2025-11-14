"""
Advanced Predictive Analytics Engine for Sarathi
Implements ML models for:
1. Vehicle health prediction and failure prevention
2. Earnings optimization and demand forecasting  
3. Driver burnout detection and health monitoring
4. Financial resilience scoring and wealth building guidance
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import pickle
import os
import logging
from dataclasses import dataclass, asdict
import joblib

# ML Libraries
from sklearn.ensemble import RandomForestRegressor, IsolationForest, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score, precision_recall_fscore_support
import xgboost as xgb
from prophet import Prophet

# Statistical Analysis
from scipy import stats
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose

logger = logging.getLogger(__name__)

@dataclass
class VehicleHealthPrediction:
    """Vehicle health prediction result"""
    health_score: float  # 0-100, higher is better
    failure_probability: float  # 0-1, probability of failure in next 30 days
    critical_components: List[str]  # Components needing immediate attention
    maintenance_priority: List[Dict[str, Any]]  # Prioritized maintenance tasks
    cost_forecast: float  # Expected maintenance cost in next 3 months
    recommended_actions: List[str]  # Specific actionable recommendations

@dataclass
class EarningsOptimization:
    """Earnings optimization prediction"""
    predicted_daily_earnings: float
    optimal_hours: List[int]  # Best hours to drive today
    location_recommendations: List[Dict[str, Any]]  # Best locations with reasoning
    demand_forecast: Dict[str, float]  # Hour-by-hour demand prediction
    weather_impact: float  # -1 to 1, impact of weather on earnings
    competitive_analysis: Dict[str, Any]  # Platform comparison and switching recommendations

@dataclass
class BurnoutRiskAssessment:
    """Driver burnout and health risk assessment"""
    burnout_risk_score: float  # 0-100, higher is more risk
    health_indicators: Dict[str, float]  # Various health metrics
    rest_recommendations: Dict[str, Any]  # When and how to rest
    workload_optimization: Dict[str, Any]  # Optimal work schedule
    intervention_needed: bool  # Whether immediate intervention is required
    support_resources: List[str]  # Available support and resources

@dataclass
class FinancialResilienceScore:
    """Financial resilience and wealth building assessment"""
    resilience_score: float  # 0-100, financial stability score
    emergency_fund_adequacy: float  # Months of expenses covered
    income_stability: float  # Income volatility measure
    growth_potential: float  # Wealth building potential
    investment_recommendations: List[Dict[str, Any]]  # Specific investment advice
    risk_factors: List[str]  # Financial risk factors to address

class VehicleHealthPredictor:
    """Predicts vehicle health and maintenance needs using ML"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.failure_predictor = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False
        self.model_path = "models/vehicle_health_model.pkl"
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load existing model or create new one"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                self.is_trained = True
                logger.info("Vehicle health model loaded successfully")
            else:
                self.model = RandomForestRegressor(n_estimators=100, random_state=42)
                logger.info("New vehicle health model created")
        except Exception as e:
            logger.error(f"Error loading vehicle health model: {str(e)}")
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    def _generate_features(self, vehicle_data: Dict[str, Any]) -> np.ndarray:
        """Generate features for vehicle health prediction"""
        features = [
            vehicle_data.get('mileage', 0),
            vehicle_data.get('km_since_last_service', 0),
            vehicle_data.get('age_in_months', 0),
            vehicle_data.get('daily_km_avg', 0),
            vehicle_data.get('engine_hours', 0),
            vehicle_data.get('brake_usage_intensity', 0.5),  # 0-1 scale
            vehicle_data.get('ac_usage_hours', 0),
            vehicle_data.get('city_driving_percentage', 0.7),  # 0-1 scale
            vehicle_data.get('maintenance_score', 0.8),  # 0-1 scale
            vehicle_data.get('fuel_efficiency', 15.0),  # km/l
        ]
        return np.array(features).reshape(1, -1)
    
    async def predict_vehicle_health(self, vehicle_data: Dict[str, Any]) -> VehicleHealthPrediction:
        """Predict vehicle health and maintenance needs"""
        try:
            features = self._generate_features(vehicle_data)
            
            # If model is not trained, use rule-based predictions
            if not self.is_trained:
                return self._rule_based_health_prediction(vehicle_data)
            
            # ML-based prediction
            scaled_features = self.scaler.transform(features)
            health_score = float(self.model.predict(scaled_features)[0])
            
            # Anomaly detection for failure prediction
            anomaly_score = self.failure_predictor.decision_function(scaled_features)[0]
            failure_probability = max(0, min(1, (50 - anomaly_score) / 100))
            
            # Determine critical components based on vehicle data
            critical_components = self._identify_critical_components(vehicle_data)
            
            # Generate maintenance priorities
            maintenance_priority = self._generate_maintenance_priorities(vehicle_data, health_score)
            
            # Forecast costs
            cost_forecast = self._forecast_maintenance_costs(vehicle_data, health_score)
            
            # Generate recommendations
            recommendations = self._generate_vehicle_recommendations(vehicle_data, health_score, failure_probability)
            
            return VehicleHealthPrediction(
                health_score=health_score,
                failure_probability=failure_probability,
                critical_components=critical_components,
                maintenance_priority=maintenance_priority,
                cost_forecast=cost_forecast,
                recommended_actions=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error predicting vehicle health: {str(e)}")
            return self._rule_based_health_prediction(vehicle_data)
    
    def _rule_based_health_prediction(self, vehicle_data: Dict[str, Any]) -> VehicleHealthPrediction:
        """Fallback rule-based prediction when ML model is not available"""
        mileage = vehicle_data.get('mileage', 0)
        km_since_service = vehicle_data.get('km_since_last_service', 0)
        age_months = vehicle_data.get('age_in_months', 0)
        
        # Calculate health score based on rules
        health_score = 100
        
        # Age factor
        if age_months > 60:
            health_score -= (age_months - 60) * 0.5
        
        # Mileage factor
        if mileage > 100000:
            health_score -= (mileage - 100000) / 1000
        
        # Service overdue factor
        if km_since_service > 5000:
            health_score -= (km_since_service - 5000) / 100
        
        health_score = max(0, min(100, health_score))
        
        # Failure probability based on service overdue and age
        failure_prob = 0.0
        if km_since_service > 8000:
            failure_prob += 0.3
        if age_months > 72:
            failure_prob += 0.2
        if mileage > 150000:
            failure_prob += 0.2
        
        failure_prob = min(1.0, failure_prob)
        
        return VehicleHealthPrediction(
            health_score=health_score,
            failure_probability=failure_prob,
            critical_components=self._identify_critical_components(vehicle_data),
            maintenance_priority=self._generate_maintenance_priorities(vehicle_data, health_score),
            cost_forecast=self._forecast_maintenance_costs(vehicle_data, health_score),
            recommended_actions=self._generate_vehicle_recommendations(vehicle_data, health_score, failure_prob)
        )
    
    def _identify_critical_components(self, vehicle_data: Dict[str, Any]) -> List[str]:
        """Identify components that need immediate attention"""
        critical = []
        
        km_since_service = vehicle_data.get('km_since_last_service', 0)
        mileage = vehicle_data.get('mileage', 0)
        
        if km_since_service > 8000:
            critical.append("Engine Oil & Filter")
        if km_since_service > 15000:
            critical.append("Brake Pads")
        if mileage > 80000 and mileage % 80000 < 5000:
            critical.append("Transmission Fluid")
        if vehicle_data.get('tire_age_months', 0) > 36:
            critical.append("Tires")
        
        return critical
    
    def _generate_maintenance_priorities(self, vehicle_data: Dict[str, Any], health_score: float) -> List[Dict[str, Any]]:
        """Generate prioritized maintenance tasks"""
        priorities = []
        
        km_since_service = vehicle_data.get('km_since_last_service', 0)
        
        if km_since_service > 5000:
            priorities.append({
                'task': 'Regular Service',
                'urgency': 'high' if km_since_service > 8000 else 'medium',
                'estimated_cost': 3000 + (km_since_service - 5000) * 0.5,
                'benefits': 'Prevents major breakdowns, maintains fuel efficiency'
            })
        
        if health_score < 70:
            priorities.append({
                'task': 'Comprehensive Inspection',
                'urgency': 'high',
                'estimated_cost': 1500,
                'benefits': 'Identify hidden issues before they become expensive'
            })
        
        return priorities
    
    def _forecast_maintenance_costs(self, vehicle_data: Dict[str, Any], health_score: float) -> float:
        """Forecast maintenance costs for next 3 months"""
        base_cost = 2000  # Base monthly maintenance
        
        # Adjust based on health score
        if health_score < 50:
            multiplier = 2.5
        elif health_score < 70:
            multiplier = 1.8
        elif health_score < 85:
            multiplier = 1.2
        else:
            multiplier = 1.0
        
        # Adjust for age and mileage
        age_factor = 1 + (vehicle_data.get('age_in_months', 0) / 120)
        mileage_factor = 1 + (vehicle_data.get('mileage', 0) / 200000)
        
        total_cost = base_cost * multiplier * age_factor * mileage_factor * 3
        return round(total_cost, 2)
    
    def _generate_vehicle_recommendations(self, vehicle_data: Dict[str, Any], health_score: float, failure_prob: float) -> List[str]:
        """Generate specific actionable recommendations"""
        recommendations = []
        
        if failure_prob > 0.3:
            recommendations.append("⚠️ URGENT: Schedule immediate professional inspection")
        
        if health_score < 60:
            recommendations.append("Consider comprehensive service package to prevent major issues")
        
        km_since_service = vehicle_data.get('km_since_last_service', 0)
        if km_since_service > 5000:
            recommendations.append(f"Schedule service - {km_since_service}km since last service")
        
        if vehicle_data.get('fuel_efficiency', 15) < 12:
            recommendations.append("Poor fuel efficiency detected - check engine and air filter")
        
        recommendations.append("Maintain detailed service records for better resale value")
        
        return recommendations

class EarningsOptimizer:
    """Optimizes driver earnings using demand prediction and market intelligence"""
    
    def __init__(self):
        self.demand_model = None
        self.price_model = None
        self.model_path = "models/earnings_optimizer.pkl"
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load or create earnings optimization models"""
        try:
            if os.path.exists(self.model_path):
                self.demand_model = joblib.load(self.model_path)
                logger.info("Earnings optimization model loaded")
            else:
                self.demand_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
                logger.info("New earnings optimization model created")
        except Exception as e:
            logger.error(f"Error loading earnings model: {str(e)}")
            self.demand_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
    
    async def optimize_earnings(self, driver_data: Dict[str, Any], current_context: Dict[str, Any]) -> EarningsOptimization:
        """Generate earnings optimization recommendations"""
        try:
            # Get current time context
            current_hour = datetime.now().hour
            current_day = datetime.now().weekday()
            
            # Predict demand for each hour of the day
            demand_forecast = self._predict_hourly_demand(current_context)
            
            # Identify optimal hours
            optimal_hours = self._identify_optimal_hours(demand_forecast, current_hour)
            
            # Generate location recommendations
            location_recommendations = self._recommend_locations(current_context, current_hour)
            
            # Assess weather impact
            weather_impact = self._assess_weather_impact(current_context.get('weather', {}))
            
            # Competitive analysis
            competitive_analysis = self._analyze_competition(current_context)
            
            # Predict daily earnings
            predicted_earnings = self._predict_daily_earnings(driver_data, current_context, demand_forecast)
            
            return EarningsOptimization(
                predicted_daily_earnings=predicted_earnings,
                optimal_hours=optimal_hours,
                location_recommendations=location_recommendations,
                demand_forecast=demand_forecast,
                weather_impact=weather_impact,
                competitive_analysis=competitive_analysis
            )
            
        except Exception as e:
            logger.error(f"Error optimizing earnings: {str(e)}")
            return self._fallback_earnings_optimization(current_context)
    
    def _predict_hourly_demand(self, context: Dict[str, Any]) -> Dict[str, float]:
        """Predict demand for each hour of the day"""
        # Base demand patterns (0-1 scale)
        base_demand = {
            0: 0.3, 1: 0.2, 2: 0.2, 3: 0.1, 4: 0.2, 5: 0.4,
            6: 0.6, 7: 0.8, 8: 0.9, 9: 0.7, 10: 0.5, 11: 0.5,
            12: 0.6, 13: 0.5, 14: 0.5, 15: 0.6, 16: 0.7, 17: 0.8,
            18: 0.9, 19: 0.8, 20: 0.7, 21: 0.6, 22: 0.6, 23: 0.4
        }
        
        # Adjust for weather
        weather = context.get('weather', {})
        if weather.get('precipitation', 0) > 0:
            # Rain increases demand
            rain_multiplier = 1 + min(weather.get('precipitation', 0) / 10, 0.5)
            base_demand = {hour: demand * rain_multiplier for hour, demand in base_demand.items()}
        
        # Adjust for day of week
        current_day = datetime.now().weekday()
        if current_day >= 5:  # Weekend
            # Later start, later end
            weekend_adjustment = {
                6: 1.2, 7: 1.1, 8: 1.0, 9: 1.1, 10: 1.2,
                20: 1.3, 21: 1.4, 22: 1.5, 23: 1.3
            }
            for hour, multiplier in weekend_adjustment.items():
                if hour in base_demand:
                    base_demand[hour] *= multiplier
        
        return base_demand
    
    def _identify_optimal_hours(self, demand_forecast: Dict[str, float], current_hour: int) -> List[int]:
        """Identify best hours to drive based on demand forecast"""
        # Sort hours by demand
        sorted_hours = sorted(demand_forecast.items(), key=lambda x: x[1], reverse=True)
        
        # Get top hours that are upcoming today
        optimal_hours = []
        for hour, demand in sorted_hours:
            if hour >= current_hour and len(optimal_hours) < 6:
                optimal_hours.append(hour)
        
        # If not enough hours today, add tomorrow's best hours
        if len(optimal_hours) < 4:
            for hour, demand in sorted_hours[:6]:
                if hour not in optimal_hours:
                    optimal_hours.append(hour)
        
        return optimal_hours[:6]
    
    def _recommend_locations(self, context: Dict[str, Any], current_hour: int) -> List[Dict[str, Any]]:
        """Recommend optimal pickup locations"""
        recommendations = []
        
        # Morning hours (6-10 AM)
        if 6 <= current_hour <= 10:
            recommendations.extend([
                {
                    'location': 'Business Districts',
                    'reasoning': 'Office commute demand peak',
                    'expected_demand': 'High',
                    'avg_fare': '₹150-250',
                    'wait_time': '2-5 minutes'
                },
                {
                    'location': 'Railway Stations',
                    'reasoning': 'Commuter connections',
                    'expected_demand': 'High',
                    'avg_fare': '₹80-150',
                    'wait_time': '1-3 minutes'
                }
            ])
        
        # Evening hours (5-9 PM)
        elif 17 <= current_hour <= 21:
            recommendations.extend([
                {
                    'location': 'Malls & Restaurants',
                    'reasoning': 'Dinner and shopping traffic',
                    'expected_demand': 'High',
                    'avg_fare': '₹120-200',
                    'wait_time': '3-7 minutes'
                },
                {
                    'location': 'Office Complexes',
                    'reasoning': 'End of workday exodus',
                    'expected_demand': 'Very High',
                    'avg_fare': '₹100-300',
                    'wait_time': '1-4 minutes'
                }
            ])
        
        # Late night (10 PM - 2 AM)
        elif current_hour >= 22 or current_hour <= 2:
            recommendations.extend([
                {
                    'location': 'Entertainment Districts',
                    'reasoning': 'Nightlife and events ending',
                    'expected_demand': 'Medium-High',
                    'avg_fare': '₹200-400',
                    'wait_time': '5-15 minutes'
                },
                {
                    'location': 'Airport',
                    'reasoning': 'Late flights and premium fares',
                    'expected_demand': 'Medium',
                    'avg_fare': '₹300-800',
                    'wait_time': '10-20 minutes'
                }
            ])
        
        return recommendations[:3]
    
    def _assess_weather_impact(self, weather_data: Dict[str, Any]) -> float:
        """Assess weather impact on earnings (-1 to 1 scale)"""
        impact = 0.0
        
        # Rain increases demand
        precipitation = weather_data.get('precipitation', 0)
        if precipitation > 0:
            impact += min(precipitation / 10, 0.4)
        
        # Extreme temperatures affect demand
        temp = weather_data.get('temperature', 25)
        if temp > 35 or temp < 10:
            impact += 0.2
        
        # Poor visibility affects safety and demand
        visibility = weather_data.get('visibility', 10)
        if visibility < 5:
            impact += 0.3
        
        return min(1.0, impact)
    
    def _analyze_competition(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competition and platform optimization"""
        return {
            'platform_recommendation': 'Ola',
            'reasoning': 'Higher surge pricing in your area',
            'surge_prediction': '1.2x expected in next hour',
            'driver_density': 'Medium - Good opportunity',
            'switching_suggestion': 'Switch to Uber after 8 PM for better rates'
        }
    
    def _predict_daily_earnings(self, driver_data: Dict[str, Any], context: Dict[str, Any], demand_forecast: Dict[str, float]) -> float:
        """Predict total daily earnings"""
        # Base calculation from driver's historical data
        avg_historical = driver_data.get('avg_daily_earnings', 1200)
        
        # Adjust for today's predicted demand
        avg_demand = sum(demand_forecast.values()) / len(demand_forecast)
        demand_multiplier = avg_demand / 0.6  # 0.6 is baseline average demand
        
        # Weather adjustment
        weather_impact = context.get('weather_impact', 0)
        weather_multiplier = 1 + weather_impact
        
        # Day of week adjustment
        day_multipliers = {0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 1.1, 5: 1.2, 6: 1.1}
        day_multiplier = day_multipliers.get(datetime.now().weekday(), 1.0)
        
        predicted = avg_historical * demand_multiplier * weather_multiplier * day_multiplier
        return round(predicted, 2)
    
    def _fallback_earnings_optimization(self, context: Dict[str, Any]) -> EarningsOptimization:
        """Fallback optimization when ML models fail"""
        current_hour = datetime.now().hour
        
        return EarningsOptimization(
            predicted_daily_earnings=1200.0,
            optimal_hours=[7, 8, 18, 19, 20, 21],
            location_recommendations=[
                {
                    'location': 'City Center',
                    'reasoning': 'Consistent demand',
                    'expected_demand': 'Medium',
                    'avg_fare': '₹150',
                    'wait_time': '5 minutes'
                }
            ],
            demand_forecast={hour: 0.5 for hour in range(24)},
            weather_impact=0.0,
            competitive_analysis={'platform_recommendation': 'Continue current platform'}
        )

class BurnoutPredictor:
    """Predicts and prevents driver burnout using health and work pattern analysis"""
    
    def __init__(self):
        self.burnout_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.health_analyzer = IsolationForest(contamination=0.15, random_state=42)
        self.model_path = "models/burnout_predictor.pkl"
        self.is_trained = False
    
    async def assess_burnout_risk(self, driver_data: Dict[str, Any]) -> BurnoutRiskAssessment:
        """Assess driver burnout risk and provide recommendations"""
        try:
            # Extract work pattern features
            work_features = self._extract_work_features(driver_data)
            health_features = self._extract_health_features(driver_data)
            
            # Calculate burnout risk score
            burnout_score = self._calculate_burnout_score(work_features, health_features)
            
            # Analyze health indicators
            health_indicators = self._analyze_health_indicators(health_features)
            
            # Generate rest recommendations
            rest_recommendations = self._generate_rest_recommendations(work_features, burnout_score)
            
            # Optimize workload
            workload_optimization = self._optimize_workload(work_features, burnout_score)
            
            # Determine if intervention is needed
            intervention_needed = burnout_score > 70 or any(
                indicator > 0.8 for indicator in health_indicators.values()
            )
            
            # Get support resources
            support_resources = self._get_support_resources(burnout_score, intervention_needed)
            
            return BurnoutRiskAssessment(
                burnout_risk_score=burnout_score,
                health_indicators=health_indicators,
                rest_recommendations=rest_recommendations,
                workload_optimization=workload_optimization,
                intervention_needed=intervention_needed,
                support_resources=support_resources
            )
            
        except Exception as e:
            logger.error(f"Error assessing burnout risk: {str(e)}")
            return self._fallback_burnout_assessment(driver_data)
    
    def _extract_work_features(self, driver_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract work pattern features"""
        return {
            'daily_hours_avg': driver_data.get('daily_hours_avg', 8.0),
            'consecutive_work_days': driver_data.get('consecutive_work_days', 5),
            'weekly_hours': driver_data.get('weekly_hours', 50),
            'break_frequency': driver_data.get('break_frequency', 3),  # breaks per day
            'sleep_hours': driver_data.get('sleep_hours', 7),
            'stress_level': driver_data.get('stress_level', 5),  # 1-10 scale
            'job_satisfaction': driver_data.get('job_satisfaction', 7)  # 1-10 scale
        }
    
    def _extract_health_features(self, driver_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract health-related features"""
        return {
            'fatigue_level': driver_data.get('fatigue_level', 5),  # 1-10 scale
            'back_pain': driver_data.get('back_pain', 3),  # 1-10 scale
            'eye_strain': driver_data.get('eye_strain', 4),  # 1-10 scale
            'appetite_change': driver_data.get('appetite_change', 0),  # -5 to 5 scale
            'mood_score': driver_data.get('mood_score', 7),  # 1-10 scale
            'concentration': driver_data.get('concentration', 8),  # 1-10 scale
            'social_withdrawal': driver_data.get('social_withdrawal', 2)  # 1-10 scale
        }
    
    def _calculate_burnout_score(self, work_features: Dict[str, float], health_features: Dict[str, float]) -> float:
        """Calculate overall burnout risk score (0-100)"""
        score = 0.0
        
        # Work pattern factors (40% of score)
        if work_features['daily_hours_avg'] > 12:
            score += 15
        elif work_features['daily_hours_avg'] > 10:
            score += 10
        
        if work_features['consecutive_work_days'] > 10:
            score += 20
        elif work_features['consecutive_work_days'] > 7:
            score += 10
        
        if work_features['sleep_hours'] < 6:
            score += 15
        elif work_features['sleep_hours'] < 7:
            score += 5
        
        # Health factors (40% of score)
        if health_features['fatigue_level'] > 7:
            score += 15
        elif health_features['fatigue_level'] > 5:
            score += 8
        
        if health_features['stress_level'] > 7:
            score += 15
        elif health_features['stress_level'] > 5:
            score += 8
        
        if health_features['mood_score'] < 4:
            score += 10
        elif health_features['mood_score'] < 6:
            score += 5
        
        # Psychological factors (20% of score)
        if work_features['job_satisfaction'] < 4:
            score += 10
        elif work_features['job_satisfaction'] < 6:
            score += 5
        
        if health_features['social_withdrawal'] > 7:
            score += 10
        
        return min(100.0, score)
    
    def _analyze_health_indicators(self, health_features: Dict[str, float]) -> Dict[str, float]:
        """Analyze individual health indicators (0-1 scale)"""
        return {
            'physical_fatigue': min(1.0, health_features['fatigue_level'] / 10),
            'mental_stress': min(1.0, health_features['stress_level'] / 10),
            'physical_pain': min(1.0, (health_features['back_pain'] + health_features['eye_strain']) / 20),
            'emotional_wellbeing': max(0.0, 1.0 - health_features['mood_score'] / 10),
            'social_health': min(1.0, health_features['social_withdrawal'] / 10)
        }
    
    def _generate_rest_recommendations(self, work_features: Dict[str, float], burnout_score: float) -> Dict[str, Any]:
        """Generate rest and recovery recommendations"""
        recommendations = {
            'immediate_rest_needed': burnout_score > 70,
            'recommended_rest_days': 0,
            'daily_break_schedule': [],
            'weekly_rest_pattern': {},
            'recovery_activities': []
        }
        
        # Determine rest days needed
        if burnout_score > 80:
            recommendations['recommended_rest_days'] = 3
        elif burnout_score > 70:
            recommendations['recommended_rest_days'] = 2
        elif burnout_score > 60:
            recommendations['recommended_rest_days'] = 1
        
        # Daily break schedule
        if work_features['break_frequency'] < 3:
            recommendations['daily_break_schedule'] = [
                {'time': '10:00 AM', 'duration': '15 minutes', 'activity': 'Walk and stretch'},
                {'time': '1:00 PM', 'duration': '30 minutes', 'activity': 'Lunch break away from vehicle'},
                {'time': '4:00 PM', 'duration': '15 minutes', 'activity': 'Hydration and eye rest'},
                {'time': '7:00 PM', 'duration': '20 minutes', 'activity': 'Evening snack and relaxation'}
            ]
        
        # Recovery activities
        if burnout_score > 60:
            recommendations['recovery_activities'] = [
                'Light exercise or walking for 30 minutes',
                'Meditation or deep breathing exercises',
                'Social activities with family/friends',
                'Hobby activities unrelated to driving',
                'Professional massage or physiotherapy if physical pain persists'
            ]
        
        return recommendations
    
    def _optimize_workload(self, work_features: Dict[str, float], burnout_score: float) -> Dict[str, Any]:
        """Optimize workload to prevent burnout"""
        optimization = {
            'recommended_daily_hours': 8,
            'max_consecutive_days': 6,
            'optimal_schedule': {},
            'workload_reduction': False
        }
        
        # Adjust recommendations based on burnout score
        if burnout_score > 70:
            optimization.update({
                'recommended_daily_hours': 6,
                'max_consecutive_days': 4,
                'workload_reduction': True,
                'gradual_increase': True
            })
        elif burnout_score > 60:
            optimization.update({
                'recommended_daily_hours': 7,
                'max_consecutive_days': 5,
                'workload_reduction': True
            })
        
        # Optimal schedule suggestions
        optimization['optimal_schedule'] = {
            'start_time': '7:00 AM',
            'end_time': f'{7 + optimization["recommended_daily_hours"]}:00 PM',
            'break_intervals': 'Every 2-3 hours',
            'weekly_rest_days': 1 if burnout_score < 60 else 2
        }
        
        return optimization
    
    def _get_support_resources(self, burnout_score: float, intervention_needed: bool) -> List[str]:
        """Get relevant support resources"""
        resources = [
            "Driver wellness helpline: 1800-XXX-XXXX",
            "Online mental health resources: sarathi-wellness.com",
            "Peer support groups for gig workers"
        ]
        
        if intervention_needed:
            resources.extend([
                "🚨 URGENT: Consider professional counseling",
                "Medical consultation for physical symptoms",
                "Financial counseling for income concerns",
                "Family support programs"
            ])
        
        if burnout_score > 60:
            resources.extend([
                "Stress management workshops",
                "Physical therapy resources for occupational health",
                "Financial planning assistance"
            ])
        
        return resources
    
    def _fallback_burnout_assessment(self, driver_data: Dict[str, Any]) -> BurnoutRiskAssessment:
        """Fallback assessment when detailed data is not available"""
        consecutive_days = driver_data.get('consecutive_work_days', 5)
        daily_hours = driver_data.get('daily_hours_avg', 8)
        
        # Simple rule-based assessment
        burnout_score = 0
        if consecutive_days > 7:
            burnout_score += 30
        if daily_hours > 10:
            burnout_score += 25
        if driver_data.get('sleep_hours', 7) < 6:
            burnout_score += 20
        
        return BurnoutRiskAssessment(
            burnout_risk_score=min(100, burnout_score),
            health_indicators={'overall_risk': burnout_score / 100},
            rest_recommendations={'immediate_rest_needed': burnout_score > 70},
            workload_optimization={'recommended_daily_hours': 8},
            intervention_needed=burnout_score > 70,
            support_resources=self._get_support_resources(burnout_score, burnout_score > 70)
        )

class AnalyticsEngine:
    """Main analytics engine that coordinates all prediction models"""
    
    def __init__(self):
        self.vehicle_predictor = VehicleHealthPredictor()
        self.earnings_optimizer = EarningsOptimizer()
        self.burnout_predictor = BurnoutPredictor()
        logger.info("Analytics Engine initialized successfully")
    
    async def get_comprehensive_insights(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive insights across all areas"""
        try:
            # Run all predictions in parallel
            vehicle_health = await self.vehicle_predictor.predict_vehicle_health(
                user_data.get('vehicle', {})
            )
            
            earnings_optimization = await self.earnings_optimizer.optimize_earnings(
                user_data.get('driver', {}),
                user_data.get('context', {})
            )
            
            burnout_assessment = await self.burnout_predictor.assess_burnout_risk(
                user_data.get('driver', {})
            )
            
            # Generate unified recommendations
            unified_insights = self._generate_unified_insights(
                vehicle_health, earnings_optimization, burnout_assessment
            )
            
            return {
                'vehicle_health': asdict(vehicle_health),
                'earnings_optimization': asdict(earnings_optimization),
                'burnout_assessment': asdict(burnout_assessment),
                'unified_insights': unified_insights,
                'timestamp': datetime.now().isoformat(),
                'confidence': self._calculate_overall_confidence(user_data)
            }
            
        except Exception as e:
            logger.error(f"Error generating comprehensive insights: {str(e)}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def _generate_unified_insights(self, vehicle_health, earnings_opt, burnout_assess) -> Dict[str, Any]:
        """Generate unified insights combining all prediction models"""
        insights = {
            'priority_actions': [],
            'risk_factors': [],
            'opportunities': [],
            'overall_resilience_score': 0
        }
        
        # Priority actions based on all models
        if vehicle_health.failure_probability > 0.5:
            insights['priority_actions'].append({
                'action': 'URGENT: Vehicle maintenance required',
                'reasoning': f'{vehicle_health.failure_probability*100:.1f}% failure probability',
                'timeline': 'Within 7 days',
                'impact': 'Critical - prevents income loss'
            })
        
        if burnout_assess.intervention_needed:
            insights['priority_actions'].append({
                'action': 'Take immediate rest days',
                'reasoning': f'High burnout risk ({burnout_assess.burnout_risk_score:.1f}/100)',
                'timeline': 'Immediately',
                'impact': 'Critical - prevents health deterioration'
            })
        
        # Opportunities
        if earnings_opt.predicted_daily_earnings > 1500:
            insights['opportunities'].append({
                'opportunity': 'High earnings potential today',
                'details': f'Predicted earnings: ₹{earnings_opt.predicted_daily_earnings}',
                'action': f'Focus on hours: {", ".join(map(str, earnings_opt.optimal_hours[:3]))}'
            })
        
        # Calculate overall resilience score
        vehicle_score = vehicle_health.health_score / 100
        health_score = 1 - (burnout_assess.burnout_risk_score / 100)
        earnings_score = min(1.0, earnings_opt.predicted_daily_earnings / 1500)
        
        insights['overall_resilience_score'] = round(
            (vehicle_score * 0.4 + health_score * 0.4 + earnings_score * 0.2) * 100, 1
        )
        
        return insights
    
    def _calculate_overall_confidence(self, user_data: Dict[str, Any]) -> float:
        """Calculate confidence in predictions based on data quality"""
        confidence = 1.0
        
        # Reduce confidence if key data is missing
        if not user_data.get('vehicle', {}):
            confidence *= 0.7
        if not user_data.get('driver', {}):
            confidence *= 0.8
        if not user_data.get('context', {}):
            confidence *= 0.9
        
        return round(confidence, 2)

# Global analytics engine instance
analytics_engine = AnalyticsEngine()