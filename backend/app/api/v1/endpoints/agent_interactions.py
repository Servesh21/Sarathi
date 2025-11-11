from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.db.database import get_db
from app.db.models import User
from app.api.v1.endpoints.auth import get_current_user
from app.agent_core.graphs.orchestrator import AgentOrchestrator

router = APIRouter()


class AgentQuery(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None


class AgentResponse(BaseModel):
    response: str
    agent_type: str
    metadata: Optional[Dict[str, Any]] = None


@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(
    agent_query: AgentQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Interact with the Sarathi agent.
    The orchestrator will route the query to the appropriate specialized agent.
    """
    try:
        orchestrator = AgentOrchestrator()
        
        # Add user context
        context = agent_query.context or {}
        context["user_id"] = current_user.id
        context["user_email"] = current_user.email
        
        # Process the query through the orchestrator
        result = await orchestrator.process_query(
            query=agent_query.query,
            context=context
        )
        
        return AgentResponse(
            response=result.get("response", ""),
            agent_type=result.get("agent_type", "general"),
            metadata=result.get("metadata", {})
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent processing error: {str(e)}"
        )


@router.post("/voice-input")
async def process_voice_input(
    audio_data: dict,
    current_user: User = Depends(get_current_user)
):
    """
    Process voice input from the user.
    This endpoint will handle speech-to-text conversion and then route to the agent.
    """
    # TODO: Implement speech-to-text processing
    # For now, return a placeholder
    return {
        "message": "Voice input processing to be implemented",
        "user_id": current_user.id
    }


@router.get("/conversation-history")
async def get_conversation_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """
    Retrieve the user's conversation history with the agent.
    """
    # TODO: Implement conversation history storage and retrieval
    return {
        "user_id": current_user.id,
        "conversations": [],
        "message": "Conversation history to be implemented"
    }
