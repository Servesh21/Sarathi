from typing import Dict, Any
from app.agents.state import AgentState
from app.agents.tools import DatabaseTool, FinancialTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.config import settings


class SurplusPlanner:
    """Node that calculates surplus and suggests allocation"""
    
    def __init__(
        self,
        db_tool: DatabaseTool,
        financial_tool: FinancialTool
    ):
        self.db_tool = db_tool
        self.financial_tool = financial_tool
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.6
        )
    
    async def __call__(self, state: AgentState) -> AgentState:
        """Calculate surplus and provide financial planning advice"""
        
        # Get financial data
        trip_stats = await self.db_tool.get_trip_stats(state['user_id'], days=30)
        goals = await self.db_tool.get_goals(state['user_id'])
        investments = await self.db_tool.get_investments(state['user_id'])
        
        # Calculate monthly income and expenses
        monthly_income = trip_stats['net_earnings']  # Last 30 days net earnings
        
        # Get user's expense data or use estimate
        monthly_expenses = state['user_profile'].get('monthly_expense_average', monthly_income * 0.6)
        
        # Calculate surplus
        surplus_analysis = self.financial_tool.calculate_surplus(
            monthly_income,
            monthly_expenses
        )
        
        recommendations = []
        
        # Goal-based recommendations
        if goals:
            total_goal_target = sum(g['target_amount'] - g['current_amount'] for g in goals)
            recommendations.append({
                'type': 'goal_allocation',
                'title': f'Allocate for {len(goals)} Active Goals',
                'description': f'₹{total_goal_target:.2f} total target remaining'
            })
        else:
            recommendations.append({
                'type': 'goal_creation',
                'title': 'Set Financial Goals',
                'description': 'Create goals like emergency fund, vehicle upgrade, or education savings.'
            })
        
        # Investment recommendations based on surplus
        if surplus_analysis['monthly_surplus'] > 1000:
            investment_suggestions = await self.financial_tool.get_investment_options(
                surplus_analysis['monthly_surplus'],
                'low'  # Default to low risk for gig workers
            )
            
            for suggestion in investment_suggestions[:2]:
                recommendations.append({
                    'type': 'investment',
                    'title': f"{suggestion['investment_type'].replace('_', ' ').title()}",
                    'description': f"Invest ₹{suggestion['suggested_amount']:.0f}/month · {suggestion['expected_return']:.1f}% returns"
                })
        
        # Emergency fund recommendation
        emergency_fund_needed = monthly_expenses * 6
        current_liquid_investments = sum(
            inv['current_value'] 
            for inv in investments 
            if inv['risk_level'] == 'low'
        )
        
        if current_liquid_investments < emergency_fund_needed:
            emergency_gap = emergency_fund_needed - current_liquid_investments
            recommendations.append({
                'type': 'emergency_fund',
                'title': 'Build Emergency Fund',
                'description': f'Target: ₹{emergency_fund_needed:.0f} · Gap: ₹{emergency_gap:.0f}'
            })
        
        # Savings rate feedback
        if surplus_analysis['surplus_percentage'] < 20:
            recommendations.append({
                'type': 'expense_reduction',
                'title': 'Increase Savings Rate',
                'description': f"Current: {surplus_analysis['surplus_percentage']:.1f}% · Target: 20%+"
            })
        
        # Update state
        state['financial_analysis'] = {
            'surplus_analysis': surplus_analysis,
            'goals': goals,
            'investments': investments,
            'emergency_fund_status': {
                'needed': emergency_fund_needed,
                'current': current_liquid_investments,
                'gap': emergency_fund_needed - current_liquid_investments
            }
        }
        state['recommendations'] = recommendations
        state['next_step'] = 'investment_advisor'
        
        return state
