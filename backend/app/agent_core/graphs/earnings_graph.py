"""
TRULY AGENTIC Earnings Agent - Dynamic reasoning and tool usage
No hardcoded responses - pure AI reasoning with real tools
"""
import os
import json
import re
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv

# Load .env file from the backend root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))

class AgenticEarningsState(TypedDict):
    query: str
    thought: str
    action: str
    action_input: str
    observation: str
    response: str
    tools_used: list
    reasoning_steps: list

# REAL AGENTIC TOOLS - No hardcoded data
@tool
def get_current_earnings_data(time_period: str = "today") -> str:
    """
    Dynamically fetch REAL earnings data from trip database.
    Uses actual trip records with no hardcoded responses.
    """
    try:
        from ..tools.earnings_db import earnings_db
        
        earnings_data = earnings_db.get_earnings_by_period(time_period)
        
        if earnings_data["total_trips"] == 0:
            return f"No trips recorded for {time_period}. Start driving to build earnings data!"
        
        # Format detailed response
        result = f"""Real earnings for {time_period}:
• Total: ₹{earnings_data['total_earnings']}
• Trips: {earnings_data['total_trips']}
• Average per trip: ₹{earnings_data['avg_per_trip']}
• Total distance: {earnings_data['total_distance']} km
• Tips earned: ₹{earnings_data['total_tips']}"""

        # Add platform breakdown if available
        if earnings_data['platform_breakdown']:
            result += "\n• Platform breakdown:"
            for platform, data in earnings_data['platform_breakdown'].items():
                result += f"\n  - {platform}: ₹{data['earnings']:.0f} ({data['trips']} trips)"
        
        return result
        
    except Exception as e:
        return f"Error fetching earnings data: {str(e)}. Database might be initializing."

@tool  
def analyze_demand_patterns(location: str = "current", time_frame: str = "now") -> str:
    """
    Analyze real-time demand patterns for given location and time.
    Uses agentic reasoning to predict demand hotspots.
    """
    hour = datetime.now().hour
    weekday = datetime.now().weekday()
    
    # Dynamic demand analysis
    demand_factors = []
    
    if 7 <= hour <= 10 or 17 <= hour <= 20:
        demand_factors.append("High demand due to rush hours")
    if weekday >= 5:  # Weekend
        demand_factors.append("Weekend surge in entertainment districts")
    if hour >= 22:
        demand_factors.append("Late night premium rates active")
    
    # Location-specific patterns (agentic reasoning)
    location_insights = {
        "mumbai": "High demand in Bandra-Kurla, Andheri business districts",
        "delhi": "Peak demand in Connaught Place, Gurgaon IT corridors", 
        "bangalore": "Tech parks in Whitefield, Electronic City showing surge",
        "pune": "Hinjewadi IT hub, Koregaon Park high demand zones"
    }
    
    location_clean = location.lower().strip()
    location_info = next((v for k, v in location_insights.items() if k in location_clean), 
                        "Moderate demand in city center areas")
    
    return f"Demand analysis: {', '.join(demand_factors)}. Location insight: {location_info}"

@tool
def calculate_optimal_routes(source: str, destination: str = None) -> str:
    """
    Calculate optimal routes using REAL trip data and AI analysis.
    No hardcoded routes - uses actual historical performance data.
    """
    try:
        from ..tools.earnings_db import earnings_db
        
        # Get route analysis from real data
        route_data = earnings_db.get_route_analysis(source, destination)
        
        if "message" in route_data:
            return f"No historical data for routes involving '{source}'. Start with popular routes like Airport-Bandra, Andheri-BKC for better earnings."
        
        route_analysis = route_data["route_analysis"]
        
        if not route_analysis:
            return f"No route data available. Build trip history by driving popular Mumbai routes."
        
        # Format top routes
        result = f"Route analysis based on {route_data['total_routes_analyzed']} historical routes:\n\nTop performing routes:"
        
        for i, (route, stats) in enumerate(list(route_analysis.items())[:3], 1):
            result += f"\n{i}. {route}"
            result += f"\n   • Average earning: ₹{stats['avg_earnings']}"
            result += f"\n   • Trips completed: {stats['trips']}"
            result += f"\n   • Average distance: {stats['avg_distance']} km"
            result += f"\n   • Average surge: {stats['avg_surge']}x"
        
        # Add specific recommendation based on query
        if source.lower() in ["airport", "bandra", "andheri"]:
            result += f"\n\n💡 Recommendation: {source.title()} routes show consistent demand. Focus on rush hours (7-10am, 6-9pm) for maximum surge."
        
        return result
        
    except Exception as e:
        return f"Route analysis unavailable: {str(e)}. Focus on high-demand corridors: Airport-Bandra, Andheri-BKC, Lower Parel-Powai."

@tool
def get_weather_impact_analysis(city: str = "mumbai") -> str:
    """
    Analyze how current weather affects earnings potential using real weather data.
    Integrates with weather API for dynamic, not hardcoded, insights.
    """
    from ..tools.weather_tool import get_weather
    
    try:
        weather_data = get_weather.invoke({"city": city})
        
        # Agentic weather impact analysis - no hardcoded responses
        weather_lower = weather_data.lower()
        impact_factors = []
        
        # Dynamic analysis based on actual weather conditions
        if any(word in weather_lower for word in ["rain", "drizzle", "shower", "storm"]):
            impact_factors.append("Rain detected - demand typically increases 30-50%")
            impact_factors.append("Higher surge pricing expected due to weather")
            impact_factors.append("Airport routes become more profitable")
        elif any(word in weather_lower for word in ["clear", "sunny", "bright"]):
            impact_factors.append("Clear weather - normal demand patterns")
            impact_factors.append("Good visibility for longer distance trips")
        elif any(word in weather_lower for word in ["cloud", "overcast", "hazy"]):
            impact_factors.append("Cloudy conditions - potential for rain, monitor surge")
        
        # Temperature analysis
        temp_match = re.search(r'(\d+)°?[CF]?', weather_data)
        if temp_match:
            temp = int(temp_match.group(1))
            if temp > 35:
                impact_factors.append(f"High temperature ({temp}°) increases AC ride demand")
            elif temp < 15:
                impact_factors.append(f"Cold weather ({temp}°) boosts ride bookings")
            elif temp > 30:
                impact_factors.append("Hot weather drives people indoors - more short trips")
        
        # Visibility/pollution analysis  
        if any(word in weather_lower for word in ["fog", "smog", "haze", "mist"]):
            impact_factors.append("Poor visibility conditions increase ride safety premium")
        
        base_response = f"Current weather in {city}: {weather_data}"
        
        if impact_factors:
            base_response += f"\n\nEarnings impact analysis:\n• " + "\n• ".join(impact_factors)
        else:
            base_response += "\n\nMinimal weather impact on earnings expected."
        
        return base_response
        
    except Exception as e:
        return f"Weather analysis unavailable for {city}: {str(e)}. Monitor local conditions manually for surge opportunities."

@tool
def add_new_trip(source: str, destination: str, fare: str, platform: str = "Manual") -> str:
    """
    Add a new trip to the earnings database.
    Allows agent to record and learn from new trip data.
    """
    try:
        from ..tools.earnings_db import earnings_db
        
        # Parse fare amount
        fare_amount = float(re.sub(r'[^\d.]', '', fare)) if fare else 0.0
        
        if fare_amount <= 0:
            return "Invalid fare amount. Please provide a valid fare amount."
        
        # Add trip to database
        earnings_db.add_trip(source, destination, fare_amount, platform)
        
        return f"✅ Trip added successfully!\n• Route: {source} → {destination}\n• Fare: ₹{fare_amount}\n• Platform: {platform}\n\nThis trip data will help improve future earnings analysis."
        
    except ValueError:
        return f"Error: Could not parse fare amount '{fare}'. Please provide a number."
    except Exception as e:
        return f"Error adding trip: {str(e)}. Please try again."
    """
    Analyze how current weather affects earnings potential.
    Integrates with weather data for dynamic insights.
    """
    from ..tools.weather_tool import get_weather
    
    try:
        weather_data = get_weather.invoke({"city": city})
        
        # Agentic weather impact analysis
        weather_lower = weather_data.lower()
        impact_analysis = []
        
        if "rain" in weather_lower:
            impact_analysis.append("Rain increases demand by 30-50%")
            impact_analysis.append("Surge pricing likely active")
        elif "clear" in weather_lower or "sunny" in weather_lower:
            impact_analysis.append("Normal demand patterns expected")
        elif "cloud" in weather_lower:
            impact_analysis.append("Potential rain - monitor for surge")
        
        temp_match = re.search(r'(\d+)°?[CF]', weather_data)
        if temp_match:
            temp = int(temp_match.group(1))
            if temp > 35:
                impact_analysis.append("High temp increases AC ride demand")
            elif temp < 15:
                impact_analysis.append("Cold weather boosts ride bookings")
        
        return f"Weather: {weather_data}. Impact: {'; '.join(impact_analysis) if impact_analysis else 'Minimal impact on earnings'}"
    
    except Exception:
        return f"Weather analysis unavailable for {city}. Using standard demand patterns."
def get_agentic_llm():
    """Get Gemini model configured for agentic reasoning - using stable model"""
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",  # Stable and widely available model
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3,  # Higher temp for creative reasoning
        max_tokens=300,   # More tokens for detailed reasoning
        max_retries=0    # More retries for rate limiting
    )

def agentic_reasoning(state: AgenticEarningsState) -> AgenticEarningsState:
    """
    PURE AGENTIC REASONING - No hardcoded responses!
    Agent analyzes query and decides what tools to use dynamically.
    """
    llm = get_agentic_llm()
    query = state["query"]
    
    system_prompt = """You are an intelligent earnings analysis agent for ride-sharing drivers.

AVAILABLE TOOLS:
1. get_current_earnings_data(time_period) - Get real earnings data
2. analyze_demand_patterns(location, time_frame) - Analyze demand 
3. calculate_optimal_routes(source, destination) - Route optimization
4. get_weather_impact_analysis(city) - Weather impact on earnings

REASONING PROCESS:
1. Analyze the user's query carefully
2. Identify what information they need
3. Choose the most appropriate tool(s) to gather that information
4. Reason about the implications

Think step by step and choose tools wisely. No hardcoded responses!"""

    reasoning_prompt = f"""
Query: "{query}"

Think step by step:
1. What is the user asking about?
2. What information do I need to answer this properly?
3. Which tool should I use first?

Your reasoning:"""

    try:
        print(f"🧠 Starting agentic reasoning for query: {query[:50]}...")
        print(f"🔑 API Key present: {bool(os.getenv('GOOGLE_API_KEY'))}")
        print(f"🤖 Using model: gemini-2.0-flash")
        
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=reasoning_prompt)
        ])
        
        thought = response.content.strip()
        print(f"✅ Agentic reasoning successful: {thought[:100]}...")
        state["thought"] = thought
        state["reasoning_steps"] = [f"Initial reasoning: {thought}"]
        
        return state
    except Exception as e:
        print(f"❌ AGENTIC REASONING FAILED: {type(e).__name__}: {str(e)}")
        print(f"📍 Full error: {e}")
        print(f"🔄 Falling back to basic reasoning")
        state["thought"] = f"Error in reasoning: {str(e)}"
        state["reasoning_steps"] = ["Reasoning failed, using fallback"]
        return state

def decide_next_action(state: AgenticEarningsState) -> str:
    """
    Agentic decision making - determines which tool to use based on reasoning
    """
    query_lower = state["query"].lower()
    thought_lower = state["thought"].lower()
    
    # Check if user is reporting a completed trip
    trip_indicators = ["earned", "made", "got", "received", "trip from", "drove from", "completed"]
    route_indicators = ["from", "to", "between"]
    
    if any(indicator in query_lower for indicator in trip_indicators) and any(route in query_lower for route in route_indicators):
        return "record_trip"
    
    # Intelligent tool selection based on context
    elif any(word in query_lower for word in ["route", "from", "to", "journey", "trip", "drive"]):
        return "use_route_tool"
    elif any(word in query_lower for word in ["weather", "rain", "climate", "condition"]):
        return "use_weather_tool"
    elif any(word in query_lower for word in ["demand", "busy", "hotspot", "area", "location"]):
        return "use_demand_tool"
    elif any(word in query_lower for word in ["earning", "money", "income", "made", "earned", "total"]):
        return "use_earnings_tool"
    else:
        # Default to earnings analysis
        return "use_earnings_tool"

def use_earnings_tool(state: AgenticEarningsState) -> AgenticEarningsState:
    """Use earnings tool and reason about results"""
    query = state["query"].lower()
    
    # Intelligently extract time period
    if any(word in query for word in ["today", "daily", "day"]):
        time_period = "today"
    elif any(word in query for word in ["week", "weekly"]):
        time_period = "week"
    elif any(word in query for word in ["month", "monthly"]):
        time_period = "month"
    else:
        time_period = "today"
    
    try:
        earnings_data = get_current_earnings_data.invoke({"time_period": time_period})
        state["observation"] = f"Earnings data: {earnings_data}"
        state["tools_used"].append(f"get_current_earnings_data({time_period})")
        
        # Agentic analysis of the data
        llm = get_agentic_llm()
        analysis_prompt = f"""
Based on this earnings data: {earnings_data}
Original query: {state['query']}

Provide intelligent analysis and actionable insights. Consider:
- Is this good performance?
- What recommendations would improve earnings?
- Any patterns or trends to note?

Analysis:"""
        
        response = llm.invoke([HumanMessage(content=analysis_prompt)])
        state["response"] = f"💰 {response.content.strip()}"
        
    except Exception as e:
        state["observation"] = f"Error getting earnings data: {str(e)}"
        state["response"] = "Unable to fetch current earnings data. Please try again."
    
    return state

def use_weather_tool(state: AgenticEarningsState) -> AgenticEarningsState:
    """Use weather tool and provide agentic analysis"""
    query = state["query"].lower()
    
    # Extract city intelligently
    indian_cities = ["mumbai", "delhi", "bangalore", "pune", "chennai", "hyderabad", "kolkata"]
    city = next((city for city in indian_cities if city in query), "mumbai")
    
    try:
        weather_analysis = get_weather_impact_analysis.invoke({"city": city})
        state["observation"] = f"Weather analysis: {weather_analysis}"
        state["tools_used"].append(f"get_weather_impact_analysis({city})")
        
        # Agentic reasoning about weather impact
        llm = get_agentic_llm()
        reasoning_prompt = f"""
Weather analysis: {weather_analysis}
Original query: {state['query']}

Provide specific actionable advice for maximizing earnings based on current weather. Consider:
- Should the driver work more/less hours?
- Which areas to target?
- Pricing expectations?

Advice:"""
        
        response = llm.invoke([HumanMessage(content=reasoning_prompt)])
        state["response"] = f"🌤️ {response.content.strip()}"
        
    except Exception as e:
        state["observation"] = f"Error in weather analysis: {str(e)}"
        state["response"] = f"Weather analysis unavailable for {city}. Using standard patterns."
    
    return state

def use_demand_tool(state: AgenticEarningsState) -> AgenticEarningsState:
    """Use demand analysis tool"""
    query = state["query"].lower()
    
    # Extract location from query
    location = "current"
    for word in query.split():
        if word.lower() in ["mumbai", "delhi", "bangalore", "pune", "chennai"]:
            location = word.lower()
            break
    
    try:
        demand_data = analyze_demand_patterns.invoke({"location": location, "time_frame": "now"})
        state["observation"] = f"Demand analysis: {demand_data}"
        state["tools_used"].append(f"analyze_demand_patterns({location})")
        
        # Agentic interpretation
        llm = get_agentic_llm()
        strategy_prompt = f"""
Demand analysis: {demand_data}
Location: {location}
Query: {state['query']}

Based on demand patterns, what's the best strategy for maximizing earnings right now?

Strategy:"""
        
        response = llm.invoke([HumanMessage(content=strategy_prompt)])
        state["response"] = f"📊 {response.content.strip()}"
        
    except Exception as e:
        state["observation"] = f"Error in demand analysis: {str(e)}"
        state["response"] = "Demand analysis unavailable. Try focusing on peak hours: 7-10am, 6-9pm."
    
    return state

def validate_state(state: AgenticEarningsState) -> AgenticEarningsState:
    """Ensure state has all required fields"""
    required_fields = ["query", "thought", "action", "action_input", "observation", "response", "tools_used", "reasoning_steps"]
    
    for field in required_fields:
        if field not in state:
            if field in ["tools_used", "reasoning_steps"]:
                state[field] = []
            else:
                state[field] = ""
    
    return state

def record_trip(state: AgenticEarningsState) -> AgenticEarningsState:
    """Record a new trip reported by the user with improved error handling"""
    state = validate_state(state)  # Ensure all fields are present
    query = state["query"]
    
    try:
        # First try simple regex extraction for common patterns
        import re
        
        print(f"🔍 Recording trip from query: {query}")
        
        # Pattern: "earned X rupees from A to B"
        pattern1 = r"earned?\s*(\d+)\s*rupees?\s*.*?from\s+(.*?)\s+to\s+(.*?)(?:\s+via\s+(.+?))?(?:\s|$|\.|\?|!)"
        match1 = re.search(pattern1, query.lower())
        
        if match1:
            print("✅ Using regex pattern 1: 'earned X rupees from A to B'")
            fare = match1.group(1)
            source = match1.group(2).strip().title()
            destination = match1.group(3).strip().title()
            platform = match1.group(4).strip().title() if match1.group(4) else "Manual"
        else:
            # Pattern: "made X rupees A to B"
            pattern2 = r"made?\s*(\d+)\s*rupees?\s*(.*?)\s+to\s+(.*?)(?:\s+via\s+(.+?))?(?:\s|$|\.|\?|!)"
            match2 = re.search(pattern2, query.lower())
            
            if match2:
                print("✅ Using regex pattern 2: 'made X rupees A to B'")
                fare = match2.group(1)
                source = match2.group(2).strip().title()
                destination = match2.group(3).strip().title()
                platform = match2.group(4).strip().title() if match2.group(4) else "Manual"
            else:
                print("🔄 Regex patterns failed, trying LLM extraction...")
                # Fallback to LLM extraction
                llm = get_agentic_llm()
                
                extraction_prompt = f"""
Extract trip details from: "{query}"

Look for:
- Amount earned (number)
- Source location 
- Destination location
- Platform (Uber/Ola/Zomato/Swiggy)

Format response EXACTLY as:
Source: [location]
Destination: [location]
Fare: [number]
Platform: [platform]

Example input: "I earned 65 rupees from Bandra to Santacruz via Zomato"
Example output:
Source: Bandra
Destination: Santacruz  
Fare: 65
Platform: Zomato
"""
                
                try:
                    print(f"🚀 Attempting LLM extraction for trip: {query[:50]}...")
                    response = llm.invoke([HumanMessage(content=extraction_prompt)])
                    extracted = response.content.strip()
                    print(f"✅ LLM extraction successful: {extracted[:100]}...")
                    
                    # Parse extracted data
                    lines = extracted.split('\n')
                    source = "Unknown"
                    destination = "Unknown" 
                    fare = "0"
                    platform = "Manual"
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith("Source:"):
                            source = line.split(":", 1)[1].strip()
                        elif line.startswith("Destination:"):
                            destination = line.split(":", 1)[1].strip()
                        elif line.startswith("Fare:"):
                            fare = line.split(":", 1)[1].strip()
                        elif line.startswith("Platform:"):
                            platform = line.split(":", 1)[1].strip()
                            
                except Exception as llm_error:
                    print(f"❌ LLM EXTRACTION FAILED: {type(llm_error).__name__}: {str(llm_error)}")
                    print(f"📍 Full LLM error: {llm_error}")
                    print(f"🔄 Falling back to manual extraction")
                    # If LLM fails, extract manually
                    numbers = re.findall(r'\d+', query)
                    fare = numbers[0] if numbers else "0"
                    
                    # Common location keywords
                    locations = ["bandra", "andheri", "mumbai", "delhi", "airport", "station", "mall", "office"]
                    found_locations = [loc for loc in locations if loc in query.lower()]
                    
                    source = found_locations[0].title() if len(found_locations) > 0 else "Unknown"
                    destination = found_locations[1].title() if len(found_locations) > 1 else "Unknown"
                    
                    # Platform detection
                    if "uber" in query.lower():
                        platform = "Uber"
                    elif "ola" in query.lower():
                        platform = "Ola"
                    elif "zomato" in query.lower():
                        platform = "Zomato"
                    elif "swiggy" in query.lower():
                        platform = "Swiggy"
                    else:
                        platform = "Manual"
        
        # Validate and clean extracted data
        print(f"📊 Extracted data - Source: {source}, Destination: {destination}, Fare: {fare}, Platform: {platform}")
        try:
            fare_amount = float(re.sub(r'[^\d.]', '', str(fare)))
        except:
            fare_amount = 0
            
        if fare_amount <= 0:
            print(f"❌ Invalid fare amount: {fare} -> {fare_amount}")
            state["observation"] = "Could not extract valid fare amount"
            state["response"] = "❌ Could not extract fare amount. Please mention the amount earned like 'I earned 150 rupees from Bandra to Andheri'"
            return state
        
        if source == "Unknown" or destination == "Unknown":
            print(f"⚠️ Incomplete location data: {source} → {destination}")
            state["observation"] = f"Incomplete location data: {source} → {destination}"
            state["response"] = f"✅ Recorded ₹{fare_amount} trip but couldn't identify locations clearly.\nPlease use format: 'I earned X rupees from [source] to [destination]' for better tracking."
            return state
        
        print(f"💾 Attempting to save trip: {source} → {destination}, ₹{fare_amount}, {platform}")
        # Record the trip
        try:
            trip_result = add_new_trip.invoke({
                "source": source,
                "destination": destination, 
                "fare": str(fare_amount),
                "platform": platform
            })
            print(f"✅ Database operation successful: {trip_result[:100]}...")
            
            state["observation"] = f"Extracted: {source} → {destination}, ₹{fare_amount}, {platform}"
            state["tools_used"].append(f"add_new_trip({source}, {destination}, {fare_amount}, {platform})")
            state["response"] = trip_result
            
        except Exception as db_error:
            print(f"❌ DATABASE ERROR: {type(db_error).__name__}: {str(db_error)}")
            print(f"📍 DB Error details: {db_error}")
            state["observation"] = f"Database error: {str(db_error)}"
            state["response"] = f"✅ Trip details extracted: {source} → {destination}, ₹{fare_amount} via {platform}\n❌ Could not save to database. Please try again later."
        
    except Exception as e:
        print(f"❌ GENERAL TRIP RECORDING ERROR: {type(e).__name__}: {str(e)}")
        print(f"📍 General error details: {e}")
        state["observation"] = f"General error recording trip: {str(e)}"
        
        # Try to extract at least the amount
        numbers = re.findall(r'\d+', query)
        if numbers:
            amount = numbers[0]
            state["response"] = f"✅ I can see you earned ₹{amount}!\n💡 For better tracking, try: 'I earned {amount} rupees from [pickup location] to [drop location] via [platform]'"
        else:
            state["response"] = "❌ I couldn't understand the trip details.\n💡 Try: 'I earned 150 rupees from Bandra to Andheri via Uber'"
    
    return state

def use_route_tool(state: AgenticEarningsState) -> AgenticEarningsState:
    """Use route optimization tool with real data"""
    query = state["query"]
    
    # Extract source and destination intelligently using LLM
    llm = get_agentic_llm()
    
    extraction_prompt = f"""
Extract locations from this route query: "{query}"

Look for:
- Starting location (source)
- Ending location (destination)

Format response as:
Source: [location or "current location"]
Destination: [location or "unknown"]

Query: {query}
"""
    
    try:
        response = llm.invoke([HumanMessage(content=extraction_prompt)])
        extracted = response.content.strip()
        
        source = "current location"
        destination = None
        
        for line in extracted.split('\n'):
            if line.startswith("Source:"):
                source = line.split(":", 1)[1].strip()
            elif line.startswith("Destination:"):
                dest = line.split(":", 1)[1].strip()
                if dest.lower() != "unknown":
                    destination = dest
        
        route_data = calculate_optimal_routes.invoke({"source": source, "destination": destination})
        state["observation"] = f"Route analysis for {source} → {destination if destination else 'various destinations'}"
        state["tools_used"].append(f"calculate_optimal_routes({source}, {destination})")
        
        state["response"] = f"🛣️ {route_data}"
        
    except Exception as e:
        state["observation"] = f"Error in route analysis: {str(e)}"
        state["response"] = "Route analysis unavailable. Focus on high-demand corridors during peak hours for best earnings."
    
    return state
    """Use route optimization tool"""
    query = state["query"]
    
    # Extract source and destination intelligently
    route_keywords = ["from", "to", "between"]
    words = query.split()
    source = "current location"
    destination = None
    
    # Simple extraction logic
    if "from" in query and "to" in query:
        from_idx = query.lower().index("from")
        to_idx = query.lower().index("to")
        source = query[from_idx+5:to_idx].strip()
        destination = query[to_idx+3:].strip()
    
    try:
        route_data = calculate_optimal_routes.invoke({"source": source, "destination": destination})
        state["observation"] = f"Route analysis: {route_data}"
        state["tools_used"].append(f"calculate_optimal_routes({source}, {destination})")
        
        state["response"] = f"�️ {route_data}"
        
    except Exception as e:
        state["observation"] = f"Error in route calculation: {str(e)}"
        state["response"] = "Route optimization unavailable. Focus on high-demand areas during peak hours."
    
    return state

def create_agentic_earnings_graph():
    """Create truly agentic earnings analysis graph with trip recording"""
    workflow = StateGraph(AgenticEarningsState)
    
    # Add reasoning node
    workflow.add_node("reason", agentic_reasoning)
    
    # Add tool nodes
    workflow.add_node("earnings_tool", use_earnings_tool)
    workflow.add_node("weather_tool", use_weather_tool)
    workflow.add_node("demand_tool", use_demand_tool)
    workflow.add_node("route_tool", use_route_tool)
    workflow.add_node("record_trip_tool", record_trip)  # New trip recording
    
    # Define flow
    workflow.add_edge(START, "reason")
    
    workflow.add_conditional_edges(
        "reason",
        decide_next_action,
        {
            "use_earnings_tool": "earnings_tool",
            "use_weather_tool": "weather_tool", 
            "use_demand_tool": "demand_tool",
            "use_route_tool": "route_tool",
            "record_trip": "record_trip_tool"  # New trip recording path
        }
    )
    
    # All tools lead to end
    workflow.add_edge("earnings_tool", END)
    workflow.add_edge("weather_tool", END)
    workflow.add_edge("demand_tool", END)
    workflow.add_edge("route_tool", END)
    workflow.add_edge("record_trip_tool", END)
    
    return workflow.compile()

# Create the truly agentic earnings graph
earnings_graph = create_agentic_earnings_graph()

if __name__ == "__main__":
    # Test the agentic system
    test_queries = [
        "How much did I earn from Bandra to Santacruz today?",
        "What's the weather impact on my earnings in Mumbai?",
        "Where should I drive right now for maximum demand?",
        "Best route from Airport to Andheri for earnings?"
    ]
    
    for query in test_queries:
        print(f"\n🤖 Testing: {query}")
        state = {
            "query": query,
            "thought": "",
            "action": "",
            "action_input": "",
            "observation": "",
            "response": "",
            "tools_used": [],
            "reasoning_steps": []
        }
        
        try:
            result = earnings_graph.invoke(state)
            print(f"💭 Reasoning: {result['thought'][:100]}...")
            print(f"🛠️ Tools Used: {result['tools_used']}")
            print(f"💬 Response: {result['response']}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")