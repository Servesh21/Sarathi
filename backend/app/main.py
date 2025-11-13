"""
Main FastAPI application entry point for Sarathi Agent API.
OPTIMIZED for hackathon deployment with LangGraph agents.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

# Import optimized agent router
try:
    from app.api.agents import router as agent_router
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False
    print("⚠️ Agent router not available - check dependencies")

# Create FastAPI application
app = FastAPI(
    title="Sarathi Agent API - OPTIMIZED",
    version="2.0.0-hackathon",
    description="Highly optimized LangGraph agents for Sarathi driving assistant",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8081", "*"],  # Include Expo dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize optimized agents on startup"""
    try:
        # Optional DB init for production
        from app.db.database import init_db
        init_db()
        print("✅ Database initialized")
    except:
        print("ℹ️ Running without database (hackathon mode)")
    
    if AGENTS_AVAILABLE:
        print("🚀 OPTIMIZED AGENTS LOADED AND READY")
        print("⚡ Performance Target: <2% error margin, maximum speed")
    else:
        print("⚠️ Agents not loaded - install requirements_optimized.txt")

@app.get("/")
async def root():
    """Root endpoint with optimization status"""
    return {
        "message": "Sarathi Agent API - OPTIMIZED FOR HACKATHON",
        "version": "2.0.0-hackathon",
        "agents_loaded": AGENTS_AVAILABLE,
        "optimization": "gemini-2.0-flash",
        "performance": "<2% error margin",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Enhanced health check with agent status"""
    status = {
        "status": "healthy",
        "agents": "loaded" if AGENTS_AVAILABLE else "unavailable",
        "optimization": "hackathon-ready"
    }
    
    if AGENTS_AVAILABLE:
        try:
            # Quick agent health check
            from app.agent_core.tools.weather_tool import get_weather
            test_weather = get_weather("Mumbai")
            status["weather_tool"] = "operational"
        except:
            status["weather_tool"] = "error"
    
    return status

# Include API routers
app.include_router(api_router, prefix=settings.API_V1_STR)

# Include optimized agent router
if AGENTS_AVAILABLE:
    app.include_router(agent_router, prefix="/api/v1/agents", tags=["agents"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="warning"  # Optimized for speed
    )
