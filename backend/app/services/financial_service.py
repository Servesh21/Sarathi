import httpx
from app.config import settings
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio


class FinancialDataService:
    """Service for fetching financial market data from Alpha Vantage"""
    
    BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(self):
        self.api_key = settings.ALPHA_VANTAGE_API_KEY
    
    async def _make_request(self, params: Dict[str, str]) -> Dict[str, Any]:
        """Make API request to Alpha Vantage"""
        params['apikey'] = self.api_key
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
    
    async def get_gold_price(self) -> Optional[Dict[str, Any]]:
        """Get current gold price"""
        try:
            # For gold, we can use commodity prices or alternative free APIs
            # Using a simplified approach with forex as proxy
            params = {
                'function': 'CURRENCY_EXCHANGE_RATE',
                'from_currency': 'XAU',  # Gold
                'to_currency': 'INR'
            }
            
            data = await self._make_request(params)
            
            if 'Realtime Currency Exchange Rate' in data:
                exchange_rate = data['Realtime Currency Exchange Rate']
                return {
                    'symbol': 'GOLD',
                    'price_per_gram': float(exchange_rate['5. Exchange Rate']) / 31.1035,  # Convert to gram
                    'currency': 'INR',
                    'last_updated': exchange_rate['6. Last Refreshed']
                }
            return None
        except Exception as e:
            print(f"Gold price fetch error: {e}")
            return None
    
    async def get_fd_rates(self) -> List[Dict[str, Any]]:
        """Get sample FD rates from major banks"""
        # Since Alpha Vantage doesn't provide FD rates, we'll provide sample data
        # In production, integrate with bank APIs or web scraping
        return [
            {
                'bank_name': 'State Bank of India',
                'tenure_months': 12,
                'interest_rate': 6.5,
                'min_amount': 1000,
                'type': 'fixed_deposit'
            },
            {
                'bank_name': 'HDFC Bank',
                'tenure_months': 12,
                'interest_rate': 7.0,
                'min_amount': 5000,
                'type': 'fixed_deposit'
            },
            {
                'bank_name': 'ICICI Bank',
                'tenure_months': 12,
                'interest_rate': 6.8,
                'min_amount': 10000,
                'type': 'fixed_deposit'
            },
            {
                'bank_name': 'Post Office',
                'tenure_months': 60,
                'interest_rate': 7.5,
                'min_amount': 1000,
                'type': 'recurring_deposit'
            }
        ]
    
    async def get_mutual_fund_recommendations(
        self,
        risk_profile: str = "low",
        amount: float = 5000
    ) -> List[Dict[str, Any]]:
        """Get mutual fund recommendations based on risk profile"""
        # Sample mutual fund data for Indian market
        all_funds = [
            {
                'fund_name': 'HDFC Liquid Fund',
                'type': 'liquid',
                'risk_level': 'low',
                'expected_return': 5.5,
                'min_investment': 5000,
                'category': 'Debt'
            },
            {
                'fund_name': 'SBI Equity Hybrid Fund',
                'type': 'hybrid',
                'risk_level': 'medium',
                'expected_return': 10.0,
                'min_investment': 5000,
                'category': 'Hybrid'
            },
            {
                'fund_name': 'ICICI Prudential Bluechip Fund',
                'type': 'equity',
                'risk_level': 'medium',
                'expected_return': 12.0,
                'min_investment': 5000,
                'category': 'Equity'
            },
            {
                'fund_name': 'Axis Long Term Equity Fund',
                'type': 'equity',
                'risk_level': 'high',
                'expected_return': 15.0,
                'min_investment': 5000,
                'category': 'ELSS'
            }
        ]
        
        # Filter based on risk profile and amount
        filtered_funds = [
            fund for fund in all_funds
            if fund['risk_level'] == risk_profile and fund['min_investment'] <= amount
        ]
        
        return filtered_funds[:3]
    
    async def get_ppf_info(self) -> Dict[str, Any]:
        """Get PPF (Public Provident Fund) information"""
        return {
            'scheme_name': 'Public Provident Fund',
            'current_interest_rate': 7.1,
            'min_investment_yearly': 500,
            'max_investment_yearly': 150000,
            'tenure_years': 15,
            'tax_benefit': 'Tax-free returns under Section 80C',
            'risk_level': 'low',
            'type': 'government_scheme'
        }
    
    async def get_nps_info(self) -> Dict[str, Any]:
        """Get NPS (National Pension System) information"""
        return {
            'scheme_name': 'National Pension System',
            'expected_return': 9.0,
            'min_investment': 1000,
            'tax_benefit': 'Additional ₹50,000 under Section 80CCD(1B)',
            'risk_level': 'medium',
            'type': 'pension_scheme'
        }
    
    async def get_investment_suggestions(
        self,
        monthly_surplus: float,
        risk_profile: str = "low",
        goal_type: str = "wealth_creation"
    ) -> List[Dict[str, Any]]:
        """Get comprehensive investment suggestions"""
        suggestions = []
        
        # Based on monthly surplus, suggest allocation
        if monthly_surplus < 2000:
            # Small surplus - focus on recurring deposits and PPF
            suggestions.append({
                'investment_type': 'recurring_deposit',
                'suggested_amount': monthly_surplus * 0.5,
                'provider': 'Post Office RD',
                'expected_return': 7.5,
                'reason': 'Safe and guaranteed returns for small amounts',
                'tenure_months': 12
            })
            suggestions.append({
                'investment_type': 'ppf',
                'suggested_amount': monthly_surplus * 0.5,
                'provider': 'Public Provident Fund',
                'expected_return': 7.1,
                'reason': 'Long-term tax-free wealth creation',
                'tenure_months': 180
            })
        elif monthly_surplus < 5000:
            # Medium surplus - mix of FD and mutual funds
            suggestions.append({
                'investment_type': 'fixed_deposit',
                'suggested_amount': monthly_surplus * 0.3,
                'provider': 'HDFC Bank FD',
                'expected_return': 7.0,
                'reason': 'Guaranteed returns with liquidity',
                'tenure_months': 12
            })
            suggestions.append({
                'investment_type': 'mutual_fund',
                'suggested_amount': monthly_surplus * 0.5,
                'provider': 'HDFC Liquid Fund',
                'expected_return': 5.5,
                'reason': 'Low-risk market-linked returns',
                'tenure_months': 6
            })
            suggestions.append({
                'investment_type': 'gold',
                'suggested_amount': monthly_surplus * 0.2,
                'provider': 'Gold Savings Scheme',
                'expected_return': 8.0,
                'reason': 'Hedge against inflation',
                'tenure_months': 12
            })
        else:
            # Higher surplus - diversified portfolio
            suggestions.append({
                'investment_type': 'mutual_fund_sip',
                'suggested_amount': monthly_surplus * 0.4,
                'provider': 'SBI Equity Hybrid Fund',
                'expected_return': 10.0,
                'reason': 'Long-term wealth creation with balanced risk',
                'tenure_months': 36
            })
            suggestions.append({
                'investment_type': 'ppf',
                'suggested_amount': monthly_surplus * 0.3,
                'provider': 'Public Provident Fund',
                'expected_return': 7.1,
                'reason': 'Tax-free retirement corpus',
                'tenure_months': 180
            })
            suggestions.append({
                'investment_type': 'fixed_deposit',
                'suggested_amount': monthly_surplus * 0.2,
                'provider': 'ICICI Bank FD',
                'expected_return': 6.8,
                'reason': 'Emergency fund with guaranteed returns',
                'tenure_months': 12
            })
            suggestions.append({
                'investment_type': 'gold',
                'suggested_amount': monthly_surplus * 0.1,
                'provider': 'Digital Gold',
                'expected_return': 8.0,
                'reason': 'Portfolio diversification',
                'tenure_months': 24
            })
        
        return suggestions
    
    async def calculate_investment_maturity(
        self,
        principal: float,
        rate: float,
        tenure_months: int,
        investment_type: str = "fixed_deposit"
    ) -> Dict[str, Any]:
        """Calculate investment maturity value"""
        rate_per_month = rate / 12 / 100
        
        if investment_type == "recurring_deposit":
            # RD formula: M = P * (1 + r) * [((1 + r)^n - 1) / r]
            n = tenure_months
            maturity_value = principal * (1 + rate_per_month) * (
                ((1 + rate_per_month) ** n - 1) / rate_per_month
            )
        else:
            # FD formula: A = P * (1 + r/n)^(n*t)
            maturity_value = principal * ((1 + rate / 100) ** (tenure_months / 12))
        
        returns = maturity_value - (principal * tenure_months if investment_type == "recurring_deposit" else principal)
        
        return {
            'principal': principal * tenure_months if investment_type == "recurring_deposit" else principal,
            'maturity_value': round(maturity_value, 2),
            'returns': round(returns, 2),
            'rate': rate,
            'tenure_months': tenure_months,
            'returns_percentage': round((returns / (principal * tenure_months if investment_type == "recurring_deposit" else principal)) * 100, 2)
        }


# Singleton instance
financial_service = FinancialDataService()
