"""
Resilience Graph - Specialized agent for weather, traffic, and route optimization.
Helps drivers make informed decisions about routes and timing.
"""
from typing import Dict, Any, Optional
from app.agent_core.tools.weather_tool import weather_tool
from app.agent_core.tools.maps_tool import maps_tool


class ResilienceGraph:
    """
    Agent specialized in route optimization, weather conditions,
    and traffic information for driver safety and efficiency.
    """
    
    def __init__(self):
        self.weather_tool = weather_tool
        self.maps_tool = maps_tool
    
    async def process(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Process resilience-related queries (weather, traffic, routes).
        
        Args:
            query: User's query
            context: Context including location, route info, etc.
        
        Returns:
            Response string
        """
        query_lower = query.lower()
        
        # Weather queries
        if "weather" in query_lower:
            # Default location or extract from query
            location = context.get("location", "Mumbai") if context else "Mumbai"
            
            if "forecast" in query_lower or "tomorrow" in query_lower or "week" in query_lower:
                weather_data = await self.weather_tool.get_weather_forecast(location, days=3)
                
                if weather_data["success"]:
                    response = f"🌤️ Weather Forecast for {location}:\n\n"
                    for i, forecast in enumerate(weather_data["forecasts"][:3]):
                        response += f"📅 {forecast['datetime']}\n"
                        response += f"   🌡️ {forecast['temperature']}°C - {forecast['description']}\n\n"
                    return response
            else:
                weather_data = await self.weather_tool.get_current_weather(location)
                
                if weather_data["success"]:
                    response = f"🌡️ Current Weather in {location}:\n\n"
                    response += f"Temperature: {weather_data['temperature']}°C\n"
                    response += f"Feels like: {weather_data['feels_like']}°C\n"
                    response += f"Conditions: {weather_data['description']}\n"
                    response += f"Humidity: {weather_data['humidity']}%\n"
                    response += f"Wind Speed: {weather_data['wind_speed']} m/s\n"
                    response += f"Visibility: {weather_data['visibility']} km"
                    return response
                else:
                    return f"Sorry, I couldn't fetch weather data: {weather_data.get('error', 'Unknown error')}"
        
        # Driving conditions check
        elif "condition" in query_lower or "safe" in query_lower:
            location = context.get("location", "Mumbai") if context else "Mumbai"
            conditions = await self.weather_tool.check_driving_conditions(location)
            
            if conditions["success"]:
                risk_emoji = {"low": "✅", "moderate": "⚠️", "high": "🛑"}
                response = f"🚦 Driving Conditions for {location}:\n\n"
                response += f"Risk Level: {conditions['risk_level'].upper()} {risk_emoji[conditions['risk_level']]}\n"
                response += f"Current: {conditions['current_conditions']}\n"
                response += f"Temperature: {conditions['temperature']}°C\n"
                response += f"Visibility: {conditions['visibility_km']} km\n\n"
                
                if conditions['warnings']:
                    response += "⚠️ Warnings:\n"
                    for warning in conditions['warnings']:
                        response += f"• {warning}\n"
                    response += f"\n{conditions['recommendation']}"
                else:
                    response += f"✅ {conditions['recommendation']}"
                
                return response
        
        # Route and traffic queries
        elif "route" in query_lower or "traffic" in query_lower:
            # Extract origin and destination if possible
            # For now, provide a template response
            response = "🗺️ Route & Traffic Information:\n\n"
            response += "I can help you with:\n"
            response += "• Find the best route between locations\n"
            response += "• Check real-time traffic conditions\n"
            response += "• Estimate trip duration\n"
            response += "• Suggest alternate routes\n\n"
            response += "Please provide your starting point and destination,\n"
            response += "and I'll find the best route for you!"
            return response
        
        # Default resilience response
        else:
            response = "🛡️ Resilience & Safety:\n\n"
            response += "I can help you with:\n"
            response += "• Weather updates & forecasts\n"
            response += "• Driving condition assessment\n"
            response += "• Route optimization\n"
            response += "• Traffic information\n\n"
            response += "Stay safe on the roads! What would you like to know?"
            return response
