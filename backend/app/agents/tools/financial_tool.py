from typing import Dict, Any, List
from app.services.financial_service import financial_service


class FinancialTool:
    """Tool for financial data and investment recommendations"""
    
    def __init__(self):
        self.financial_service = financial_service
    
    async def get_investment_options(
        self,
        monthly_surplus: float,
        risk_profile: str = "low"
    ) -> List[Dict[str, Any]]:
        """Get investment options based on surplus and risk profile"""
        suggestions = await self.financial_service.get_investment_suggestions(
            monthly_surplus,
            risk_profile,
            "wealth_creation"
        )
        
        return suggestions
    
    async def get_fd_rates(self) -> List[Dict[str, Any]]:
        """Get current FD rates"""
        return await self.financial_service.get_fd_rates()
    
    async def get_mutual_funds(
        self,
        risk_profile: str,
        amount: float
    ) -> List[Dict[str, Any]]:
        """Get mutual fund recommendations"""
        return await self.financial_service.get_mutual_fund_recommendations(
            risk_profile,
            amount
        )
    
    async def calculate_returns(
        self,
        principal: float,
        rate: float,
        tenure_months: int,
        investment_type: str
    ) -> Dict[str, Any]:
        """Calculate investment returns"""
        return await self.financial_service.calculate_investment_maturity(
            principal,
            rate,
            tenure_months,
            investment_type
        )
    
    async def get_gold_price(self) -> Dict[str, Any]:
        """Get current gold price"""
        gold_data = await self.financial_service.get_gold_price()
        return gold_data if gold_data else {'price_per_gram': 0, 'currency': 'INR'}
    
    async def get_ppf_info(self) -> Dict[str, Any]:
        """Get PPF scheme information"""
        return await self.financial_service.get_ppf_info()
    
    async def get_nps_info(self) -> Dict[str, Any]:
        """Get NPS scheme information"""
        return await self.financial_service.get_nps_info()
    
    def calculate_surplus(
        self,
        monthly_income: float,
        monthly_expenses: float
    ) -> Dict[str, Any]:
        """Calculate monthly surplus and provide analysis"""
        surplus = monthly_income - monthly_expenses
        surplus_percentage = (surplus / monthly_income * 100) if monthly_income > 0 else 0
        
        # Recommended allocation: 50% savings, 30% investments, 20% emergency fund
        recommended_savings = surplus * 0.5
        recommended_investments = surplus * 0.3
        recommended_emergency = surplus * 0.2
        
        # Emergency fund status
        emergency_fund_target = monthly_expenses * 6  # 6 months of expenses
        
        insights = []
        
        if surplus <= 0:
            insights.append("Your expenses exceed income. Focus on reducing costs.")
        elif surplus < 2000:
            insights.append("Small surplus. Start with recurring deposits.")
        elif surplus < 5000:
            insights.append("Good surplus. Consider mix of FD and mutual funds.")
        else:
            insights.append("Excellent surplus. Diversify across multiple instruments.")
        
        if surplus_percentage < 10:
            insights.append("Try to save at least 20% of your income.")
        elif surplus_percentage > 50:
            insights.append("Great savings rate! Consider higher-return investments.")
        
        return {
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'monthly_surplus': surplus,
            'surplus_percentage': surplus_percentage,
            'recommended_savings': recommended_savings,
            'recommended_investments': recommended_investments,
            'recommended_emergency': recommended_emergency,
            'emergency_fund_target': emergency_fund_target,
            'insights': insights
        }
