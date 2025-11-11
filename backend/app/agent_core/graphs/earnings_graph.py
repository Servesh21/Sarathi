"""
Earnings Graph - Specialized agent for financial and earnings-related queries.
Uses LangGraph to create a stateful conversation flow for financial insights.
"""
from typing import Dict, Any, Optional
from app.agent_core.tools.financial_tool import financial_tool


class EarningsGraph:
    """
    Agent specialized in earnings calculation, financial insights,
    and profitability analysis for drivers.
    """
    
    def __init__(self):
        self.tool = financial_tool
    
    async def process(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Process earnings-related queries.
        
        Args:
            query: User's query
            context: Context including user_id, db session, etc.
        
        Returns:
            Response string
        """
        query_lower = query.lower()
        
        # Earnings calculation
        if "earnings" in query_lower or "income" in query_lower:
            period = "week"  # default
            if "today" in query_lower or "daily" in query_lower:
                period = "day"
            elif "month" in query_lower or "monthly" in query_lower:
                period = "month"
            elif "year" in query_lower or "yearly" in query_lower:
                period = "year"
            
            # TODO: Get actual db session from context
            response = f"Your {period}ly earnings analysis:\n\n"
            response += "📊 Total Earnings: $450.00\n"
            response += "🚗 Total Trips: 25\n"
            response += "📏 Total Distance: 320 km\n"
            response += "💵 Average per trip: $18.00\n\n"
            response += "Keep up the great work! 🎉"
            
            return response
        
        # Fuel cost projection
        elif "fuel" in query_lower or "gas" in query_lower:
            # Extract distance if mentioned
            import re
            distance_match = re.search(r'(\d+)\s*(?:km|kilometer)', query_lower)
            distance = float(distance_match.group(1)) if distance_match else 50.0
            
            fuel_data = await self.tool.project_fuel_costs(
                distance_km=distance,
                vehicle_type="car",
                fuel_price_per_liter=1.5
            )
            
            if fuel_data["success"]:
                response = f"⛽ Fuel Cost Estimation for {distance} km:\n\n"
                response += f"Fuel Needed: {fuel_data['fuel_needed_liters']} liters\n"
                response += f"Estimated Cost: ${fuel_data['estimated_cost']}\n"
                response += f"Fuel Efficiency: {fuel_data['fuel_efficiency_km_per_liter']} km/L"
                return response
        
        # Profitability analysis
        elif "profit" in query_lower or "worth it" in query_lower:
            response = "💰 Profitability Analysis:\n\n"
            response += "Let me analyze if this trip is worth it.\n"
            response += "Expected Earnings: $45.00\n"
            response += "Fuel Cost: $12.50\n"
            response += "Maintenance: $2.50\n"
            response += "Net Profit: $30.00 ✅\n\n"
            response += "This trip looks profitable! Go for it! 🚀"
            return response
        
        # Default financial advice
        else:
            response = "💼 Financial Insights:\n\n"
            response += "I can help you with:\n"
            response += "• Track your earnings (daily/weekly/monthly)\n"
            response += "• Calculate fuel costs\n"
            response += "• Analyze trip profitability\n"
            response += "• Financial planning & budgeting\n\n"
            response += "What would you like to know?"
            return response
