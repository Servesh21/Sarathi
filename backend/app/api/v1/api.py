from fastapi import APIRouter
from app.api.v1.endpoints import auth, agent_interactions, user_profile

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(agent_interactions.router, prefix="/agent", tags=["agent"])
api_router.include_router(user_profile.router, prefix="/users", tags=["users"])
