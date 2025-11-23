from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from app.config import settings
import chromadb
from chromadb.config import Settings as ChromaSettings

# SQLAlchemy Async Engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    poolclass=NullPool,
    future=True
)

# Session Factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base Model
Base = declarative_base()


# Dependency for DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ChromaDB Client
def get_chroma_client():
    """Get ChromaDB client for vector storage"""
    try:
        client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        return client
    except Exception as e:
        # Fallback to persistent client for local development
        client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        return client


# Initialize Collections
def init_chroma_collections():
    """Initialize ChromaDB collections for different use cases"""
    client = get_chroma_client()
    
    collections = {
        "trip_patterns": "Stores trip patterns and earnings data for pattern matching",
        "vehicle_diagnostics": "Stores vehicle diagnostic history and recommendations",
        "financial_advice": "Stores financial advice and investment recommendations",
        "user_context": "Stores user conversation context and preferences"
    }
    
    for collection_name, description in collections.items():
        try:
            client.get_or_create_collection(
                name=collection_name,
                metadata={"description": description}
            )
        except Exception as e:
            print(f"Error creating collection {collection_name}: {e}")
    
    return client
