from typing import Dict, Any
from app.agents.state import AgentState
from app.agents.tools import FinancialTool
from app.services import gemini_service
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.config import settings


class InvestmentAdvisor:
    """Node that provides investment recommendations"""
    
    def __init__(self, financial_tool: FinancialTool):
        self.financial_tool = financial_tool
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.6
        )
    
    async def __call__(self, state: AgentState) -> AgentState:
        """Provide personalized investment recommendations"""
        
        surplus_analysis = state['financial_analysis']['surplus_analysis']
        goals = state['financial_analysis']['goals']
        
        monthly_surplus = surplus_analysis['monthly_surplus']
        
        if monthly_surplus <= 0:
            response = "Your current expenses meet or exceed your income. Focus on reducing costs or increasing earnings before investing. I can help you identify high-demand zones to boost your income!"
            state['response'] = response
            state['action_items'] = ["Reduce expenses", "Increase trip earnings"]
            state['messages'].append(AIMessage(content=response))
            state['next_step'] = 'end'
            return state
        
        # Get investment options
        investment_options = await self.financial_tool.get_investment_options(
            monthly_surplus,
            'low'  # Conservative for gig workers
        )
        
        # Get specific product information
        fd_rates = await self.financial_tool.get_fd_rates()
        ppf_info = await self.financial_tool.get_ppf_info()
        gold_price = await self.financial_tool.get_gold_price()
        
        # Generate comprehensive financial plan
        financial_plan = await gemini_service.generate_financial_plan(
            state['user_profile'],
            goals,
            {
                'monthly_income': surplus_analysis['monthly_income'],
                'monthly_expenses': surplus_analysis['monthly_expenses'],
                'monthly_surplus': monthly_surplus,
                'current_investments': state['financial_analysis']['investments']
            }
        )
        
        # Build detailed recommendations with calculations
        detailed_recommendations = []
        
        for option in investment_options[:3]:
            # Calculate maturity
            if option.get('suggested_amount', 0) > 0:
                tenure_months = option.get('tenure_months', 12)
                investment_type = option['investment_type']
                
                calc_result = await self.financial_tool.calculate_returns(
                    option['suggested_amount'],
                    option['expected_return'],
                    tenure_months,
                    investment_type
                )
                
                detailed_recommendations.append({
                    'type': 'investment_option',
                    'title': option['provider'],
                    'investment_type': investment_type,
                    'monthly_amount': option['suggested_amount'],
                    'expected_return': option['expected_return'],
                    'tenure_months': tenure_months,
                    'maturity_value': calc_result.get('maturity_value', 0),
                    'total_returns': calc_result.get('returns', 0),
                    'reason': option['reason']
                })
        
        state['recommendations'] = detailed_recommendations
        
        # Generate natural language response
        response_prompt = f"""Provide personalized investment advice based on this financial situation:

Monthly Surplus: ₹{monthly_surplus:.2f}
Savings Rate: {surplus_analysis['surplus_percentage']:.1f}%

Recommended Allocation:
- Savings: ₹{surplus_analysis['recommended_savings']:.2f}
- Investments: ₹{surplus_analysis['recommended_investments']:.2f}
- Emergency Fund: ₹{surplus_analysis['recommended_emergency']:.2f}

Top Investment Options:
{chr(10).join([f"- {r['title']}: ₹{r['monthly_amount']:.0f}/month · {r['expected_return']:.1f}% · Maturity: ₹{r['maturity_value']:.0f}" for r in detailed_recommendations])}

Active Goals: {len(goals)}

Provide clear, actionable investment advice. Be encouraging and supportive. Keep it concise (4-5 sentences)."""
        
        messages = state['messages'] + [
            SystemMessage(content="You are Sarathi, a financial advisor helping drivers build wealth. Provide clear, low-risk investment guidance."),
            HumanMessage(content=response_prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        state['response'] = response.content
        state['action_items'] = [r['title'] for r in detailed_recommendations[:3]]
        state['messages'].append(AIMessage(content=response.content))
        state['next_step'] = 'end'
        
        return state
