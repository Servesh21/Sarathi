"""
LangGraph Orchestrator for Sarathi Agent
Routes user queries to appropriate specialized agents (graphs).
"""
from typing import Dict, Any, Optional
import re


class AgentOrchestrator:
    """
    Main orchestrator that routes queries to specialized agent graphs.
    Uses pattern matching and intent detection to determine the appropriate agent.
    """
    
    def __init__(self):
        self.earnings_keywords = ["earnings", "income", "profit", "revenue", "money", "financial"]
        self.resilience_keywords = ["weather", "traffic", "route", "navigation", "condition", "safety"]
        self.garage_keywords = ["vehicle", "car", "garage", "maintenance"]
    
    async def detect_intent(self, query: str) -> str:
        """
        Detect the intent of the user query.
        
        Args:
            query: User's query string
        
        Returns:
            Intent type (earnings, resilience, garage, general)
        """
        query_lower = query.lower()
        
        # Check for earnings/financial intent
        if any(keyword in query_lower for keyword in self.earnings_keywords):
            return "earnings"
        
        # Check for resilience intent (weather, traffic, routing)
        if any(keyword in query_lower for keyword in self.resilience_keywords):
            return "resilience"
        
        # Check for garage/vehicle intent
        if any(keyword in query_lower for keyword in self.garage_keywords):
            return "garage"
        
        # Default to general
        return "general"
    
    async def process_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a user query by routing to the appropriate agent.
        
        Args:
            query: User's query
            context: Additional context (user_id, location, etc.)
        
        Returns:
            Agent response with metadata
        """
        intent = await self.detect_intent(query)
        
        # Route to appropriate agent
        if intent == "earnings":
            from app.agent_core.graphs.earnings_graph import EarningsGraph
            agent = EarningsGraph()
            response = await agent.process(query, context)
            return {
                "response": response,
                "agent_type": "earnings",
                "metadata": {"intent": intent}
            }
        
        elif intent == "resilience":
            from app.agent_core.graphs.resilience_graph import ResilienceGraph
            agent = ResilienceGraph()
            response = await agent.process(query, context)
            return {
                "response": response,
                "agent_type": "resilience",
                "metadata": {"intent": intent}
            }
        
        else:
            # General response
            return {
                "response": "I'm Sarathi, your driving companion. I can help you with:\n\n"
                           "💰 Earnings & Financial Planning\n"
                           "🛡️ Route Optimization & Weather Updates\n"
                           "🚗 Vehicle Management\n\n"
                           "How can I assist you today?",
                "agent_type": "general",
                "metadata": {"intent": intent}
            }
    
    async def handle_multi_intent(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle queries that may involve multiple intents.
        
        Args:
            query: User's query
            context: Additional context
        
        Returns:
            Combined response from multiple agents
        """
        # TODO: Implement multi-intent handling with LangGraph
        # For now, use single intent detection
        return await self.process_query(query, context)
