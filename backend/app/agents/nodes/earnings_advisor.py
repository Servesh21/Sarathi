from typing import Dict, Any
from app.agents.state import AgentState
from app.agents.tools import DatabaseTool, MapsTool, ChromaTool
from app.services import gemini_service
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.config import settings
from datetime import datetime


class EarningsAdvisor:
    """Node that provides earnings optimization advice"""
    
    def __init__(
        self,
        db_tool: DatabaseTool,
        maps_tool: MapsTool,
        chroma_tool: ChromaTool
    ):
        self.db_tool = db_tool
        self.maps_tool = maps_tool
        self.chroma_tool = chroma_tool
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.7
        )
    
    async def __call__(self, state: AgentState) -> AgentState:
        """Provide earnings optimization recommendations"""
        
        # Get comprehensive trip data
        trip_history = await self.db_tool.get_trip_history(state['user_id'], days=30)
        trip_stats = await self.db_tool.get_trip_stats(state['user_id'], days=30)
        
        # Get user's current location (use last trip or city center)
        if trip_history:
            last_trip = trip_history[0]
            current_location = (
                last_trip.get('end_lat', 12.9716),
                last_trip.get('end_lng', 77.5946)
            )
        else:
            # Default to Bangalore city center
            current_location = (12.9716, 77.5946)
        
        # Get high-demand zones
        high_demand_zones = self.maps_tool.get_high_demand_zones(
            current_location,
            state['user_profile'].get('city', 'Bangalore')
        )
        
        # Analyze earnings pattern using Gemini
        analysis = await gemini_service.analyze_earnings_pattern(
            trip_history[:10],  # Last 10 trips
            {
                'total_trips': trip_stats['total_trips'],
                'avg_earnings': trip_stats['avg_earnings'],
                'city': state['user_profile'].get('city', 'Bangalore')
            }
        )
        
        # Build comprehensive response
        recommendations = []
        
        # Zone recommendations
        if high_demand_zones:
            top_zone = high_demand_zones[0]
            recommendations.append({
                'type': 'high_demand_zone',
                'title': f"Head to {top_zone['zone_name']}",
                'description': f"Expected earnings: ₹{top_zone['expected_earnings']:.0f}",
                'details': top_zone
            })
        
        # Earnings insights
        if trip_stats['total_trips'] > 0:
            avg_earnings = trip_stats['avg_earnings']
            if avg_earnings < 100:
                recommendations.append({
                    'type': 'earnings_improvement',
                    'title': 'Increase Trip Distance',
                    'description': f"Your average earnings (₹{avg_earnings:.0f}) are low. Focus on longer trips or premium areas."
                })
            
            # Net profit analysis
            net_earnings = trip_stats['net_earnings']
            if net_earnings < trip_stats['total_earnings'] * 0.6:
                recommendations.append({
                    'type': 'cost_reduction',
                    'title': 'Reduce Operating Costs',
                    'description': f"Your profit margin is low. Review fuel efficiency and route optimization."
                })
        
        # Time-based recommendations
        current_hour = datetime.now().hour
        if 5 <= current_hour < 9:
            recommendations.append({
                'type': 'peak_hour',
                'title': 'Morning Peak Hour',
                'description': 'High demand for office commuters. Focus on transit stations and business districts.'
            })
        elif 17 <= current_hour < 21:
            recommendations.append({
                'type': 'peak_hour',
                'title': 'Evening Peak Hour',
                'description': 'High demand for return commutes. Target residential areas and entertainment zones.'
            })
        
        # Update state
        state['earnings_analysis'] = {
            'stats': trip_stats,
            'analysis': analysis,
            'zones': high_demand_zones[:3]
        }
        state['recommendations'] = recommendations
        
        # Generate natural language response
        response_prompt = f"""Based on the following earnings data and analysis, provide clear, actionable advice to the driver:

Trip Statistics:
- Total trips (30 days): {trip_stats['total_trips']}
- Total earnings: ₹{trip_stats['total_earnings']:.2f}
- Average per trip: ₹{trip_stats['avg_earnings']:.2f}
- Net earnings: ₹{trip_stats['net_earnings']:.2f}

Top Recommendations:
{chr(10).join([f"- {r['title']}: {r['description']}" for r in recommendations[:3]])}

High-Demand Zones:
{chr(10).join([f"- {z['zone_name']} ({z['expected_earnings']:.0f} expected)" for z in high_demand_zones[:3]])}

Provide a friendly, encouraging response with specific actionable steps. Keep it concise (3-4 sentences)."""
        
        messages = state['messages'] + [
            SystemMessage(content="You are Sarathi, a helpful AI advisor for drivers. Provide clear, actionable earnings optimization advice."),
            HumanMessage(content=response_prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        state['response'] = response.content
        state['action_items'] = [r['title'] for r in recommendations[:3]]
        state['messages'].append(AIMessage(content=response.content))
        state['next_step'] = 'end'
        
        return state
