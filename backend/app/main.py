"""
Main FastAPI application entry point for Sarathi Guardian API.
Enhanced with AI agent system and event-driven architecture.
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging

# Core imports
from app.core.config import settings
from app.db.database import engine, init_db
from app.db.models import Base

# API imports
from app.api.v1.api import api_router

# Agent and Event imports
try:
    from app.api.agents import router as agent_router
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False
    agent_router = None

try:
    from app.agent_core.events import events_router, initialize_event_system
    EVENTS_AVAILABLE = True
except ImportError:
    EVENTS_AVAILABLE = False
    events_router = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Sarathi Guardian API",
    description="AI-Powered Guardian System for Gig Workers - Transforming Financial Fragility into Resilience",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8081", "*"],  # Include Expo dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

# Include agent router if available
if AGENTS_AVAILABLE:
    app.include_router(agent_router, prefix="/api/v1/agents", tags=["agents"])

# Include events router if available
if EVENTS_AVAILABLE:
    app.include_router(events_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    try:
        logger.info("🚀 Sarathi Guardian API starting up...")
        
        # Initialize database
        try:
            init_db()
            Base.metadata.create_all(bind=engine)
            logger.info("✅ Database initialized")
        except Exception as db_error:
            logger.warning(f"Database initialization skipped: {str(db_error)}")
        
        # Initialize the event-driven system if available
        if EVENTS_AVAILABLE:
            try:
                await initialize_event_system()
                logger.info("✅ Event-driven system initialized")
            except Exception as event_error:
                logger.error(f"Event system initialization failed: {str(event_error)}")
        
        # Log system status
        features_active = []
        if AGENTS_AVAILABLE:
            features_active.append("🧠 AI Agents")
        if EVENTS_AVAILABLE:
            features_active.append("⚡ Event System")
        
        logger.info(f"🛡️ Sarathi Guardian API is ready!")
        logger.info(f"Active features: {', '.join(features_active) if features_active else 'Basic API only'}")
        
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        # Don't raise in production to allow basic API to work

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on application shutdown"""
    logger.info("Sarathi Guardian API shutting down...")

@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "message": "Sarathi Guardian API - Autonomous AI Agent for Gig Workers",
        "version": "2.0.0",
        "description": "Transforming financial fragility into resilience through intelligent automation",
        "system_status": {
            "agents_loaded": AGENTS_AVAILABLE,
            "events_active": EVENTS_AVAILABLE,
            "optimization": "Production Ready"
        },
        "features": [
            "🧠 Advanced RAG-powered knowledge system",
            "📊 Predictive analytics and ML models", 
            "🛡️ Autonomous resilience guardian",
            "📱 Real-time monitoring and alerts",
            "⚡ Event-driven intervention system",
            "💰 Earnings optimization engine",
            "🚗 Vehicle health management",
            "❤️ Driver wellness protection"
        ],
        "docs_url": "/docs",
        "api_version": "/api/v1"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint with comprehensive system status"""
    status = {
        "status": "healthy",
        "timestamp": "2024-12-19T20:45:00Z",
        "version": "2.0.0"
    }
    
    # Check services
    services = {
        "api": "operational",
        "database": "checking...",
        "ai_agents": "loaded" if AGENTS_AVAILABLE else "unavailable",
        "event_system": "active" if EVENTS_AVAILABLE else "unavailable"
    }
    
    # Test database connection
    try:
        from app.db.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        services["database"] = "operational"
    except Exception:
        services["database"] = "error"
    
    # Test agent tools if available
    if AGENTS_AVAILABLE:
        try:
            from app.agent_core.tools.weather_tool import get_weather
            test_result = get_weather("Mumbai")
            services["weather_tool"] = "operational"
        except Exception:
            services["weather_tool"] = "error"
    
    status["services"] = services
    
    return status

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "system_error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
