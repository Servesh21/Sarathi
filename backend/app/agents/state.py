from typing import TypedDict, Annotated, List, Dict, Any
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    """State that is passed between nodes in the agent graph"""
    
    # User context
    user_id: int
    user_profile: Dict[str, Any]
    
    # Current request
    query: str
    query_type: str  # earnings, vehicle, financial, general
    
    # Messages history
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Tool outputs
    trip_data: List[Dict[str, Any]]
    vehicle_data: Dict[str, Any]
    financial_data: Dict[str, Any]
    map_data: Dict[str, Any]
    
    # Analysis results
    earnings_analysis: Dict[str, Any]
    vehicle_analysis: Dict[str, Any]
    financial_analysis: Dict[str, Any]
    
    # Recommendations
    recommendations: List[Dict[str, Any]]
    
    # Final response
    response: str
    action_items: List[str]
    
    # Control flow
    next_step: str
    requires_human_input: bool
