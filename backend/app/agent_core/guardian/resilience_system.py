"""
Sarathi Resilience Guardian System
Autonomous system designed to transform financial fragility into resilience
Prevents disasters, maximizes earnings, and builds long-term wealth for gig workers
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json
import math

# Internal imports
from ..knowledge.rag_system import knowledge_base
from ..analytics.predictive_engine import analytics_engine
from ..graphs.advanced_orchestrator import guardian_agent

logger = logging.getLogger(__name__)

class ResilienceLevel(Enum):
    """Driver resilience levels"""
    FRAGILE = 1      # High risk, needs immediate intervention
    VULNERABLE = 2   # Some risks, needs monitoring
    STABLE = 3       # Good situation, minor optimizations needed
    RESILIENT = 4    # Strong position, focus on growth
    ANTIFRAGILE = 5  # Thriving, helping others

class InterventionUrgency(Enum):
    """Intervention urgency levels"""
    CRITICAL = 1     # Must act within hours
    URGENT = 2       # Must act within days  
    IMPORTANT = 3    # Should act within week
    BENEFICIAL = 4   # Good to do when convenient

@dataclass
class ResilienceMetrics:
    """Comprehensive resilience scoring"""
    overall_score: float        # 0-100 resilience score
    financial_stability: float  # Emergency fund, income stability
    income_optimization: float  # Earnings efficiency
    asset_protection: float     # Vehicle health, insurance
    health_sustainability: float # Physical and mental health
    growth_trajectory: float    # Wealth building progress
    risk_mitigation: float      # Risk prevention measures
    
@dataclass
class GuardianIntervention:
    """Autonomous guardian intervention"""
    intervention_id: str
    urgency: InterventionUrgency
    category: str  # 'financial', 'health', 'vehicle', 'earnings', 'growth'
    title: str
    description: str
    immediate_actions: List[str]
    long_term_plan: List[str]
    expected_impact: str
    timeline: str
    auto_executable: bool
    requires_confirmation: bool
    cost_estimate: float
    benefit_estimate: float

@dataclass
class WealthBuildingPlan:
    """Long-term wealth building strategy"""
    current_net_worth: float
    monthly_income_avg: float
    monthly_expenses_avg: float
    savings_rate: float
    emergency_fund_months: float
    investment_portfolio: Dict[str, float]
    debt_obligations: Dict[str, float]
    wealth_goals: List[Dict[str, Any]]
    next_milestone: Dict[str, Any]
    growth_strategy: List[str]

class ResilienceGuardian:
    """
    The core autonomous system that protects and grows gig worker wealth
    Acts as a 24/7 financial and operational guardian
    """
    
    def __init__(self):
        self.active_interventions = {}
        self.resilience_history = {}
        self.guardian_rules = self._initialize_guardian_rules()
        logger.info("Resilience Guardian System initialized")
    
    def _initialize_guardian_rules(self) -> Dict[str, Any]:
        """Initialize the core guardian rules and thresholds"""
        return {
            # Critical financial thresholds
            'emergency_fund_minimum': 30000,  # ₹30k absolute minimum
            'daily_earnings_floor': 800,      # Below this triggers intervention
            'vehicle_health_critical': 50,    # Health score below 50% is critical
            'burnout_risk_max': 70,          # Burnout score above 70% needs intervention
            
            # Growth targets
            'monthly_savings_target': 0.20,   # 20% of income should be saved
            'emergency_fund_target': 3.0,     # 3 months of expenses
            'wealth_growth_rate': 0.12,       # 12% annual growth target
            
            # Auto-intervention triggers
            'auto_savings_threshold': 5000,   # Auto-save when balance > ₹5k
            'maintenance_alert_km': 4500,     # Alert at 4500km since service
            'rest_day_trigger': 12,           # Force rest after 12 consecutive days
            
            # Protection rules
            'max_daily_hours': 14,            # Never allow more than 14h/day
            'min_sleep_hours': 6,             # Enforce minimum sleep
            'max_risk_exposure': 0.30,        # Max 30% of wealth in risky investments
        }
    
    async def assess_resilience(self, user_data: Dict[str, Any]) -> ResilienceMetrics:
        """Comprehensive resilience assessment"""
        try:
            # Get comprehensive analytics
            analytics_data = await analytics_engine.get_comprehensive_insights(user_data)
            
            # Calculate individual metric scores
            financial_score = self._assess_financial_stability(user_data, analytics_data)
            income_score = self._assess_income_optimization(user_data, analytics_data)
            asset_score = self._assess_asset_protection(user_data, analytics_data)
            health_score = self._assess_health_sustainability(user_data, analytics_data)
            growth_score = self._assess_growth_trajectory(user_data, analytics_data)
            risk_score = self._assess_risk_mitigation(user_data, analytics_data)
            
            # Calculate weighted overall score
            overall_score = (
                financial_score * 0.25 +
                income_score * 0.20 +
                asset_score * 0.15 +
                health_score * 0.15 +
                growth_score * 0.15 +
                risk_score * 0.10
            )
            
            return ResilienceMetrics(
                overall_score=round(overall_score, 1),
                financial_stability=financial_score,
                income_optimization=income_score,
                asset_protection=asset_score,
                health_sustainability=health_score,
                growth_trajectory=growth_score,
                risk_mitigation=risk_score
            )
            
        except Exception as e:
            logger.error(f"Error assessing resilience: {str(e)}")
            return self._fallback_resilience_metrics()
    
    async def generate_interventions(
        self, 
        user_data: Dict[str, Any], 
        resilience_metrics: ResilienceMetrics
    ) -> List[GuardianIntervention]:
        """Generate autonomous guardian interventions"""
        try:
            interventions = []
            
            # Critical financial interventions
            if resilience_metrics.financial_stability < 30:
                interventions.extend(await self._critical_financial_interventions(user_data))
            
            # Vehicle protection interventions
            if resilience_metrics.asset_protection < 50:
                interventions.extend(await self._vehicle_protection_interventions(user_data))
            
            # Health protection interventions
            if resilience_metrics.health_sustainability < 40:
                interventions.extend(await self._health_protection_interventions(user_data))
            
            # Income optimization interventions
            if resilience_metrics.income_optimization < 60:
                interventions.extend(await self._income_optimization_interventions(user_data))
            
            # Growth building interventions
            if resilience_metrics.growth_trajectory < 70:
                interventions.extend(await self._growth_building_interventions(user_data))
            
            # Sort by urgency
            interventions.sort(key=lambda x: x.urgency.value)
            
            return interventions[:10]  # Limit to top 10 interventions
            
        except Exception as e:
            logger.error(f"Error generating interventions: {str(e)}")
            return []
    
    async def execute_autonomous_actions(
        self, 
        user_id: str, 
        interventions: List[GuardianIntervention]
    ) -> Dict[str, Any]:
        """Execute autonomous actions that don't require user confirmation"""
        try:
            executed_actions = []
            pending_confirmations = []
            
            for intervention in interventions:
                if intervention.auto_executable and not intervention.requires_confirmation:
                    # Execute immediately
                    result = await self._execute_intervention(intervention, user_id)
                    executed_actions.append({
                        'intervention_id': intervention.intervention_id,
                        'action': intervention.title,
                        'result': result,
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    # Queue for user confirmation
                    pending_confirmations.append({
                        'intervention_id': intervention.intervention_id,
                        'title': intervention.title,
                        'description': intervention.description,
                        'urgency': intervention.urgency.name,
                        'estimated_benefit': intervention.benefit_estimate,
                        'estimated_cost': intervention.cost_estimate
                    })
            
            return {
                'executed_actions': executed_actions,
                'pending_confirmations': pending_confirmations,
                'autonomous_protection_active': len(executed_actions) > 0
            }
            
        except Exception as e:
            logger.error(f"Error executing autonomous actions: {str(e)}")
            return {'error': str(e)}
    
    async def create_wealth_building_plan(self, user_data: Dict[str, Any]) -> WealthBuildingPlan:
        """Create comprehensive wealth building strategy"""
        try:
            # Extract financial data
            financial_data = user_data.get('financial', {})
            driver_data = user_data.get('driver', {})
            
            # Calculate current financial position
            monthly_income = financial_data.get('monthly_income_avg', 35000)
            monthly_expenses = financial_data.get('monthly_expenses_avg', 25000)
            savings_rate = max(0, (monthly_income - monthly_expenses) / monthly_income)
            
            emergency_fund = financial_data.get('emergency_fund', 15000)
            emergency_fund_months = emergency_fund / monthly_expenses if monthly_expenses > 0 else 0
            
            # Current investments and assets
            vehicle_value = financial_data.get('vehicle_value', 500000)
            bank_balance = financial_data.get('bank_balance', 25000)
            investments = financial_data.get('investments', {})
            debts = financial_data.get('debts', {})
            
            current_net_worth = vehicle_value + bank_balance + sum(investments.values()) - sum(debts.values())
            
            # Generate wealth goals based on current situation
            wealth_goals = self._generate_wealth_goals(current_net_worth, monthly_income, savings_rate)
            
            # Create growth strategy
            growth_strategy = await self._create_growth_strategy(
                monthly_income, savings_rate, emergency_fund_months
            )
            
            return WealthBuildingPlan(
                current_net_worth=current_net_worth,
                monthly_income_avg=monthly_income,
                monthly_expenses_avg=monthly_expenses,
                savings_rate=savings_rate,
                emergency_fund_months=emergency_fund_months,
                investment_portfolio=investments,
                debt_obligations=debts,
                wealth_goals=wealth_goals,
                next_milestone=wealth_goals[0] if wealth_goals else {},
                growth_strategy=growth_strategy
            )
            
        except Exception as e:
            logger.error(f"Error creating wealth building plan: {str(e)}")
            return self._fallback_wealth_plan()
    
    # Assessment methods
    def _assess_financial_stability(self, user_data: Dict[str, Any], analytics: Dict[str, Any]) -> float:
        """Assess financial stability (0-100)"""
        try:
            financial_data = user_data.get('financial', {})
            
            # Emergency fund adequacy (40% of score)
            emergency_fund = financial_data.get('emergency_fund', 0)
            monthly_expenses = financial_data.get('monthly_expenses_avg', 25000)
            emergency_months = emergency_fund / monthly_expenses if monthly_expenses > 0 else 0
            emergency_score = min(100, (emergency_months / 3.0) * 100)
            
            # Income stability (30% of score)
            income_variance = financial_data.get('income_variance', 0.3)  # 0-1 scale
            stability_score = max(0, (1 - income_variance) * 100)
            
            # Debt-to-income ratio (20% of score)
            monthly_income = financial_data.get('monthly_income_avg', 35000)
            monthly_debt = financial_data.get('monthly_debt_payments', 0)
            debt_ratio = monthly_debt / monthly_income if monthly_income > 0 else 0
            debt_score = max(0, (1 - min(1, debt_ratio * 2)) * 100)
            
            # Liquidity (10% of score)
            liquid_assets = financial_data.get('bank_balance', 0) + financial_data.get('emergency_fund', 0)
            liquidity_score = min(100, (liquid_assets / 50000) * 100)
            
            final_score = (
                emergency_score * 0.4 +
                stability_score * 0.3 +
                debt_score * 0.2 +
                liquidity_score * 0.1
            )
            
            return round(final_score, 1)
            
        except Exception as e:
            logger.error(f"Error assessing financial stability: {str(e)}")
            return 50.0
    
    def _assess_income_optimization(self, user_data: Dict[str, Any], analytics: Dict[str, Any]) -> float:
        """Assess income optimization efficiency (0-100)"""
        try:
            driver_data = user_data.get('driver', {})
            earnings_data = analytics.get('earnings_optimization', {})
            
            # Current vs potential earnings (50% of score)
            current_daily = driver_data.get('daily_earnings_avg', 1200)
            potential_daily = earnings_data.get('predicted_daily_earnings', 1200)
            efficiency_ratio = current_daily / potential_daily if potential_daily > 0 else 1
            efficiency_score = min(100, efficiency_ratio * 100)
            
            # Hours vs earnings ratio (30% of score)
            daily_hours = driver_data.get('daily_hours_avg', 10)
            hourly_rate = current_daily / daily_hours if daily_hours > 0 else 0
            target_hourly = 120  # ₹120/hour target
            hourly_score = min(100, (hourly_rate / target_hourly) * 100)
            
            # Platform optimization (20% of score)
            platform_efficiency = driver_data.get('platform_efficiency', 0.7)  # 0-1 scale
            platform_score = platform_efficiency * 100
            
            final_score = (
                efficiency_score * 0.5 +
                hourly_score * 0.3 +
                platform_score * 0.2
            )
            
            return round(final_score, 1)
            
        except Exception as e:
            logger.error(f"Error assessing income optimization: {str(e)}")
            return 60.0
    
    def _assess_asset_protection(self, user_data: Dict[str, Any], analytics: Dict[str, Any]) -> float:
        """Assess asset protection and vehicle health (0-100)"""
        try:
            vehicle_data = user_data.get('vehicle', {})
            vehicle_health = analytics.get('vehicle_health', {})
            
            # Vehicle health score (60% of score)
            health_score = vehicle_health.get('health_score', 80)
            
            # Insurance coverage (25% of score)
            has_comprehensive = vehicle_data.get('comprehensive_insurance', False)
            insurance_score = 100 if has_comprehensive else 30
            
            # Maintenance regularity (15% of score)
            maintenance_score = vehicle_data.get('maintenance_score', 70)
            
            final_score = (
                health_score * 0.6 +
                insurance_score * 0.25 +
                maintenance_score * 0.15
            )
            
            return round(final_score, 1)
            
        except Exception as e:
            logger.error(f"Error assessing asset protection: {str(e)}")
            return 70.0
    
    def _assess_health_sustainability(self, user_data: Dict[str, Any], analytics: Dict[str, Any]) -> float:
        """Assess driver health and sustainability (0-100)"""
        try:
            driver_data = user_data.get('driver', {})
            burnout_data = analytics.get('burnout_assessment', {})
            
            # Burnout risk (40% of score)
            burnout_risk = burnout_data.get('burnout_risk_score', 30)
            burnout_score = max(0, 100 - burnout_risk)
            
            # Work-life balance (30% of score)
            consecutive_days = driver_data.get('consecutive_work_days', 6)
            work_balance_score = max(0, 100 - (consecutive_days - 6) * 10)
            
            # Physical health indicators (20% of score)
            sleep_hours = driver_data.get('sleep_hours', 7)
            sleep_score = min(100, (sleep_hours / 8) * 100)
            
            # Stress management (10% of score)
            stress_level = driver_data.get('stress_level', 5)  # 1-10 scale
            stress_score = max(0, (10 - stress_level) / 10 * 100)
            
            final_score = (
                burnout_score * 0.4 +
                work_balance_score * 0.3 +
                sleep_score * 0.2 +
                stress_score * 0.1
            )
            
            return round(final_score, 1)
            
        except Exception as e:
            logger.error(f"Error assessing health sustainability: {str(e)}")
            return 65.0
    
    def _assess_growth_trajectory(self, user_data: Dict[str, Any], analytics: Dict[str, Any]) -> float:
        """Assess wealth building and growth trajectory (0-100)"""
        try:
            financial_data = user_data.get('financial', {})
            
            # Savings rate (40% of score)
            savings_rate = financial_data.get('savings_rate', 0.15)
            savings_score = min(100, (savings_rate / 0.25) * 100)  # 25% target
            
            # Investment diversification (30% of score)
            investments = financial_data.get('investments', {})
            investment_total = sum(investments.values())
            monthly_income = financial_data.get('monthly_income_avg', 35000)
            investment_ratio = investment_total / (monthly_income * 12) if monthly_income > 0 else 0
            investment_score = min(100, (investment_ratio / 0.5) * 100)  # 50% of annual income target
            
            # Financial goal progress (20% of score)
            goal_progress = financial_data.get('goal_progress', 0.3)  # 0-1 scale
            goal_score = goal_progress * 100
            
            # Learning and skill development (10% of score)
            skill_development = financial_data.get('skill_development', 0.5)  # 0-1 scale
            skill_score = skill_development * 100
            
            final_score = (
                savings_score * 0.4 +
                investment_score * 0.3 +
                goal_score * 0.2 +
                skill_score * 0.1
            )
            
            return round(final_score, 1)
            
        except Exception as e:
            logger.error(f"Error assessing growth trajectory: {str(e)}")
            return 45.0
    
    def _assess_risk_mitigation(self, user_data: Dict[str, Any], analytics: Dict[str, Any]) -> float:
        """Assess risk mitigation measures (0-100)"""
        try:
            # Emergency preparedness (40% of score)
            has_emergency_plan = user_data.get('emergency_plan', False)
            emergency_score = 80 if has_emergency_plan else 20
            
            # Insurance coverage (30% of score)
            vehicle_data = user_data.get('vehicle', {})
            has_health_insurance = user_data.get('health_insurance', False)
            has_vehicle_insurance = vehicle_data.get('comprehensive_insurance', False)
            insurance_score = (
                (50 if has_health_insurance else 0) +
                (50 if has_vehicle_insurance else 0)
            )
            
            # Diversification (20% of score)
            platforms_used = len(user_data.get('platforms', ['ola']))
            diversification_score = min(100, (platforms_used / 3) * 100)
            
            # Financial buffer (10% of score)
            financial_data = user_data.get('financial', {})
            buffer_months = financial_data.get('emergency_fund', 0) / financial_data.get('monthly_expenses_avg', 25000)
            buffer_score = min(100, (buffer_months / 6) * 100)
            
            final_score = (
                emergency_score * 0.4 +
                insurance_score * 0.3 +
                diversification_score * 0.2 +
                buffer_score * 0.1
            )
            
            return round(final_score, 1)
            
        except Exception as e:
            logger.error(f"Error assessing risk mitigation: {str(e)}")
            return 50.0
    
    # Intervention generation methods
    async def _critical_financial_interventions(self, user_data: Dict[str, Any]) -> List[GuardianIntervention]:
        """Generate critical financial interventions"""
        interventions = []
        financial_data = user_data.get('financial', {})
        
        # Emergency fund critical low
        emergency_fund = financial_data.get('emergency_fund', 0)
        if emergency_fund < self.guardian_rules['emergency_fund_minimum']:
            interventions.append(GuardianIntervention(
                intervention_id=f"emergency_fund_critical_{datetime.now().strftime('%Y%m%d%H%M')}",
                urgency=InterventionUrgency.CRITICAL,
                category='financial',
                title='🚨 Emergency Fund Critical Low',
                description=f'Emergency fund is ₹{emergency_fund}, below critical minimum of ₹{self.guardian_rules["emergency_fund_minimum"]}',
                immediate_actions=[
                    'Stop all non-essential spending immediately',
                    'Work additional hours this week',
                    'Sell unused items for quick cash',
                    'Set up automatic savings of ₹1000/week minimum'
                ],
                long_term_plan=[
                    'Build emergency fund to ₹50,000 over 6 months',
                    'Create multiple income streams',
                    'Reduce fixed expenses by 15%'
                ],
                expected_impact='Prevents financial catastrophe during emergencies',
                timeline='Immediate action required',
                auto_executable=False,
                requires_confirmation=True,
                cost_estimate=0,
                benefit_estimate=50000
            ))
        
        return interventions
    
    async def _vehicle_protection_interventions(self, user_data: Dict[str, Any]) -> List[GuardianIntervention]:
        """Generate vehicle protection interventions"""
        interventions = []
        vehicle_data = user_data.get('vehicle', {})
        
        # Vehicle health critical
        km_since_service = vehicle_data.get('km_since_last_service', 0)
        if km_since_service > self.guardian_rules['maintenance_alert_km']:
            interventions.append(GuardianIntervention(
                intervention_id=f"vehicle_maintenance_{datetime.now().strftime('%Y%m%d%H%M')}",
                urgency=InterventionUrgency.URGENT,
                category='vehicle',
                title='🔧 Vehicle Maintenance Overdue',
                description=f'Vehicle has driven {km_since_service}km since last service',
                immediate_actions=[
                    'Schedule service appointment within 3 days',
                    'Check engine oil and fluid levels daily',
                    'Avoid long-distance trips until serviced',
                    'Keep ₹5000 ready for service costs'
                ],
                long_term_plan=[
                    'Set up automatic service reminders',
                    'Build vehicle maintenance fund',
                    'Find trusted mechanic for regular relationship'
                ],
                expected_impact='Prevents expensive breakdowns and income loss',
                timeline='Within 3 days',
                auto_executable=False,
                requires_confirmation=True,
                cost_estimate=3500,
                benefit_estimate=15000
            ))
        
        return interventions
    
    async def _health_protection_interventions(self, user_data: Dict[str, Any]) -> List[GuardianIntervention]:
        """Generate health protection interventions"""
        interventions = []
        driver_data = user_data.get('driver', {})
        
        # Consecutive work days exceeded
        consecutive_days = driver_data.get('consecutive_work_days', 0)
        if consecutive_days > self.guardian_rules['rest_day_trigger']:
            interventions.append(GuardianIntervention(
                intervention_id=f"mandatory_rest_{datetime.now().strftime('%Y%m%d%H%M')}",
                urgency=InterventionUrgency.CRITICAL,
                category='health',
                title='🛑 Mandatory Rest Required',
                description=f'You have worked {consecutive_days} consecutive days without rest',
                immediate_actions=[
                    'Take complete rest for next 24 hours',
                    'No driving or work-related activities',
                    'Focus on sleep and recovery',
                    'Light exercise like walking only'
                ],
                long_term_plan=[
                    'Establish weekly rest day schedule',
                    'Monitor burnout indicators',
                    'Consider health insurance if not covered'
                ],
                expected_impact='Prevents burnout and maintains long-term earning capacity',
                timeline='Immediate - next 24 hours',
                auto_executable=True,
                requires_confirmation=False,
                cost_estimate=1200,  # One day earnings lost
                benefit_estimate=10000  # Prevention of burnout
            ))
        
        return interventions
    
    async def _income_optimization_interventions(self, user_data: Dict[str, Any]) -> List[GuardianIntervention]:
        """Generate income optimization interventions"""
        interventions = []
        driver_data = user_data.get('driver', {})
        
        # Low daily earnings pattern
        daily_avg = driver_data.get('daily_earnings_avg', 1200)
        if daily_avg < self.guardian_rules['daily_earnings_floor']:
            interventions.append(GuardianIntervention(
                intervention_id=f"earnings_optimization_{datetime.now().strftime('%Y%m%d%H%M')}",
                urgency=InterventionUrgency.URGENT,
                category='earnings',
                title='📈 Earnings Below Target',
                description=f'Daily average ₹{daily_avg} is below minimum target of ₹{self.guardian_rules["daily_earnings_floor"]}',
                immediate_actions=[
                    'Focus on peak hours: 8-10 AM, 6-9 PM',
                    'Position near business districts',
                    'Use multiple platforms (Ola + Uber)',
                    'Track surge pricing patterns'
                ],
                long_term_plan=[
                    'Analyze weekly earning patterns',
                    'Optimize route knowledge',
                    'Consider delivery services during off-peak',
                    'Build customer rating for better rides'
                ],
                expected_impact='Increase daily earnings by ₹300-500',
                timeline='Implement today',
                auto_executable=True,
                requires_confirmation=False,
                cost_estimate=0,
                benefit_estimate=10000  # Monthly improvement
            ))
        
        return interventions
    
    async def _growth_building_interventions(self, user_data: Dict[str, Any]) -> List[GuardianIntervention]:
        """Generate wealth building interventions"""
        interventions = []
        financial_data = user_data.get('financial', {})
        
        # Low savings rate
        savings_rate = financial_data.get('savings_rate', 0.1)
        if savings_rate < 0.15:  # Below 15% savings rate
            interventions.append(GuardianIntervention(
                intervention_id=f"wealth_building_{datetime.now().strftime('%Y%m%d%H%M')}",
                urgency=InterventionUrgency.IMPORTANT,
                category='growth',
                title='💰 Wealth Building Acceleration',
                description=f'Savings rate of {savings_rate*100:.1f}% is below recommended 20%',
                immediate_actions=[
                    'Set up automatic transfer of ₹2000/week to savings',
                    'Track all expenses for one week',
                    'Identify and cut one unnecessary expense',
                    'Open high-interest savings account'
                ],
                long_term_plan=[
                    'Build to 25% savings rate over 6 months',
                    'Start SIP investment of ₹3000/month',
                    'Learn about investment options',
                    'Set wealth building goals'
                ],
                expected_impact='Build wealth foundation for long-term security',
                timeline='Start this week',
                auto_executable=True,
                requires_confirmation=False,
                cost_estimate=0,
                benefit_estimate=50000  # Annual benefit
            ))
        
        return interventions
    
    # Utility methods
    def _generate_wealth_goals(
        self, 
        current_net_worth: float, 
        monthly_income: float, 
        savings_rate: float
    ) -> List[Dict[str, Any]]:
        """Generate realistic wealth building goals"""
        goals = []
        
        # Emergency fund goal (if not met)
        emergency_target = monthly_income * 2.5 * 3  # 3 months of expenses
        if current_net_worth < emergency_target:
            goals.append({
                'title': 'Emergency Fund',
                'target_amount': emergency_target,
                'current_amount': current_net_worth * 0.3,  # Estimate 30% is liquid
                'timeline_months': 12,
                'priority': 1,
                'description': 'Build 3-month emergency fund for financial security'
            })
        
        # Vehicle upgrade/replacement fund
        goals.append({
            'title': 'Vehicle Upgrade Fund',
            'target_amount': 200000,
            'current_amount': 0,
            'timeline_months': 24,
            'priority': 2,
            'description': 'Save for vehicle down payment or upgrade'
        })
        
        # Long-term wealth building
        goals.append({
            'title': 'Wealth Building Portfolio',
            'target_amount': 500000,
            'current_amount': current_net_worth * 0.1,  # Estimate 10% in investments
            'timeline_months': 60,
            'priority': 3,
            'description': 'Build investment portfolio for long-term growth'
        })
        
        return goals
    
    async def _create_growth_strategy(
        self, 
        monthly_income: float, 
        savings_rate: float, 
        emergency_months: float
    ) -> List[str]:
        """Create personalized growth strategy"""
        strategy = []
        
        if emergency_months < 1:
            strategy.append("🔴 PRIORITY: Build emergency fund to ₹30,000 immediately")
        elif emergency_months < 3:
            strategy.append("🟡 Focus: Complete 3-month emergency fund")
        else:
            strategy.append("🟢 Strength: Good emergency fund, focus on growth")
        
        if savings_rate < 0.15:
            strategy.append("📊 Increase savings rate to 20% through expense optimization")
        elif savings_rate < 0.25:
            strategy.append("📈 Good savings rate, optimize investment allocation")
        else:
            strategy.append("⭐ Excellent saver, consider advanced investment strategies")
        
        # Always include these universal strategies
        strategy.extend([
            "🚗 Maintain vehicle health to protect primary income asset",
            "📱 Use technology to optimize earnings and track expenses",
            "🎯 Set specific monthly savings targets and track progress",
            "📚 Continuously learn about financial planning and investment",
            "🤝 Build network with other successful drivers for tips and opportunities"
        ])
        
        return strategy
    
    async def _execute_intervention(self, intervention: GuardianIntervention, user_id: str) -> str:
        """Execute a specific intervention"""
        try:
            # Log the intervention execution
            logger.info(f"Executing intervention {intervention.intervention_id} for user {user_id}")
            
            # Here you would implement actual intervention execution
            # For now, we'll simulate execution
            
            execution_results = []
            
            for action in intervention.immediate_actions:
                # Simulate action execution
                if "automatic" in action.lower() or "set up" in action.lower():
                    execution_results.append(f"✅ {action} - Automated")
                elif "alert" in action.lower() or "reminder" in action.lower():
                    execution_results.append(f"🔔 {action} - Alert set")
                else:
                    execution_results.append(f"📝 {action} - Logged for user action")
            
            return f"Intervention executed: {len(execution_results)} actions processed"
            
        except Exception as e:
            logger.error(f"Error executing intervention: {str(e)}")
            return f"Intervention execution failed: {str(e)}"
    
    def _fallback_resilience_metrics(self) -> ResilienceMetrics:
        """Fallback resilience metrics when assessment fails"""
        return ResilienceMetrics(
            overall_score=50.0,
            financial_stability=50.0,
            income_optimization=60.0,
            asset_protection=70.0,
            health_sustainability=65.0,
            growth_trajectory=45.0,
            risk_mitigation=50.0
        )
    
    def _fallback_wealth_plan(self) -> WealthBuildingPlan:
        """Fallback wealth building plan"""
        return WealthBuildingPlan(
            current_net_worth=400000,
            monthly_income_avg=35000,
            monthly_expenses_avg=25000,
            savings_rate=0.15,
            emergency_fund_months=1.5,
            investment_portfolio={},
            debt_obligations={},
            wealth_goals=[],
            next_milestone={},
            growth_strategy=["Build emergency fund", "Increase savings rate", "Maintain vehicle health"]
        )

# Global resilience guardian instance
resilience_guardian = ResilienceGuardian()