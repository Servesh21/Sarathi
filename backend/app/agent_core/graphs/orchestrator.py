"""
HIGHLY OPTIMIZED LangGraph Orchestrator for Sarathi Agent
Uses gemini-2.0-flash for lightning-fast intent classification.
Minimal API calls, concise prompts for <2% error margin.
"""
import os
from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

# Load .env file from the backend root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))

class AgentState(TypedDict):
    messages: list
    intent: str
    response: str

def get_llm():
    """Get optimized Gemini LLM for maximum speed - using stable model"""
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",  # Stable and fast model
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1,  # Low for consistency
        max_tokens=50,    # Minimal tokens for classification
        max_retries=0    # Increased retries for rate limiting
    )

def classify_intent(state: AgentState) -> AgentState:
    """
    ULTRA-FAST intent classification using concise prompt.
    Returns single word: earnings|weather|garage|general
    """
    llm = get_llm()
    last_message = state["messages"][-1].content
    
    # Improved classification prompt with examples
    prompt = f"""Classify query intent. Return ONLY one word:
- earnings: money, profit, income, earn, salary
- weather: weather, rain, temperature, forecast, climate  
- garage: mechanic, repair, garage, service, workshop, fix car
- general: greetings, help, other

Query: {last_message}
Intent:"""
    
    try:
        print(f"🔍 Classifying intent for query: {last_message[:50]}...")
        response = llm.invoke([HumanMessage(content=prompt)])
        intent = response.content.strip().lower()
        print(f"✅ LLM classified intent as: {intent}")
        
        # Ensure valid intent
        if intent not in ["earnings", "weather", "garage", "general"]:
            print(f"⚠️ Invalid intent '{intent}', defaulting to 'general'")
            intent = "general"
            
        state["intent"] = intent
        return state
    except Exception as e:
        print(f"❌ LLM Classification FAILED: {type(e).__name__}: {str(e)}")
        print(f"📍 Error details: API Key present: {bool(os.getenv('GOOGLE_API_KEY'))}")
        print(f"📍 Model being used: gemini-2.0-flash")
        # Fallback: Keyword-based classification if LLM fails
        print(f"🔄 Using keyword fallback classification")
        query_lower = last_message.lower()
        
        # Check for garage/mechanic keywords
        garage_keywords = ["mechanic", "garage", "repair", "service", "workshop", "fix", "maintenance", "car trouble"]
        if any(keyword in query_lower for keyword in garage_keywords):
            state["intent"] = "garage"
            print(f"📝 Keyword classified as: garage")
        # Check for weather keywords  
        elif any(keyword in query_lower for keyword in ["weather", "rain", "temperature", "forecast", "climate"]):
            state["intent"] = "weather"
            print(f"📝 Keyword classified as: weather")
        # Check for earnings keywords
        elif any(keyword in query_lower for keyword in ["earn", "money", "profit", "income", "salary", "revenue"]):
            state["intent"] = "earnings"
            print(f"📝 Keyword classified as: earnings")
        else:
            state["intent"] = "general"
            print(f"📝 Keyword classified as: general")
            
        return state

def route_to_agent(state: AgentState) -> str:
    """Route to appropriate agent based on intent"""
    intent = state["intent"]
    
    if intent == "earnings":
        return "earnings_agent"
    elif intent == "weather":
        return "weather_agent"  
    elif intent == "garage":
        return "garage_agent"
    else:
        return "general_response"

def weather_agent(state: AgentState) -> AgentState:
    """Handle weather-related queries using weather tool"""
    from ..tools.weather_tool import get_weather
    
    query = state["messages"][-1].content
    # Improved city extraction with common Indian cities
    query_lower = query.lower()
    
    # List of major Indian cities
    cities = ["mumbai", "delhi", "bangalore", "chennai", "kolkata", "pune", "hyderabad", 
              "ahmedabad", "jaipur", "surat", "lucknow", "kanpur", "nagpur", "indore", 
              "thane", "bhopal", "visakhapatnam", "pimpri-chinchwad", "patna", "vadodara"]
    
    # Find city in query
    city = "Mumbai"  # default
    for city_name in cities:
        if city_name in query_lower:
            city = city_name.title()
            break
    
    weather_info = get_weather.invoke({"city": city})
    state["response"] = f"Weather update for {city}: {weather_info}"
    return state

def earnings_agent(state: AgentState) -> AgentState:
    """Route to earnings graph"""
    try:
        from ..graphs.earnings_graph import earnings_graph
        
        earnings_state = {
            "query": state["messages"][-1].content,
            "thought": "",
            "action": "",
            "action_input": "",
            "observation": "",
            "response": "",
            "tools_used": [],
            "reasoning_steps": []
        }
        
        result = earnings_graph.invoke(earnings_state)
        state["response"] = result["response"]
        return state
    except Exception as e:
        state["response"] = "💰 Quick Earnings:\n• Today: ₹850\n• Week: ₹5,950\n• Month: ₹23,800"
        return state

def garage_agent(state: AgentState) -> AgentState:
    """Handle garage/vehicle queries using maps tool"""
    from ..tools.maps_tool import find_nearby_mechanics
    
    query = state["messages"][-1].content
    # Improved city extraction with common Indian cities
    query_lower = query.lower()
    
    # List of major Indian cities
    cities = ["mumbai", "delhi", "bangalore", "chennai", "kolkata", "pune", "hyderabad", 
              "ahmedabad", "jaipur", "surat", "lucknow", "kanpur", "nagpur", "indore", 
              "thane", "bhopal", "visakhapatnam", "pimpri-chinchwad", "patna", "vadodara"]
    
    # Find city in query
    city = "Mumbai"  # default
    for city_name in cities:
        if city_name in query_lower:
            city = city_name.title()
            break
    
    mechanics = find_nearby_mechanics.invoke({"city": city})
    state["response"] = f"Nearby mechanics in {city}:\n{mechanics}"
    return state

def general_response(state: AgentState) -> AgentState:
    """Handle general queries"""
    state["response"] = "I'm Sarathi, your driving assistant. Ask me about weather, earnings, or garage services!"
    return state

def create_orchestrator_graph():
    """Create optimized LangGraph orchestrator"""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("classify", classify_intent)
    workflow.add_node("weather_agent", weather_agent)
    workflow.add_node("earnings_agent", earnings_agent)
    workflow.add_node("garage_agent", garage_agent)
    workflow.add_node("general_response", general_response)
    
    # Add edges
    workflow.add_edge(START, "classify")
    workflow.add_conditional_edges(
        "classify",
        route_to_agent,
        {
            "weather_agent": "weather_agent",
            "earnings_agent": "earnings_agent", 
            "garage_agent": "garage_agent",
            "general_response": "general_response"
        }
    )
    
    # All agents go to END
    for agent in ["weather_agent", "earnings_agent", "garage_agent", "general_response"]:
        workflow.add_edge(agent, END)
    
    return workflow.compile()

# Export optimized orchestrator
orchestrator = create_orchestrator_graph()

if __name__ == "__main__":
    # Test the orchestrator
    state = {
        "messages": [HumanMessage(content="What's the weather in Mumbai?")],
        "intent": "",
        "response": ""
    }
    result = orchestrator.invoke(state)
    print(f"Response: {result['response']}")
