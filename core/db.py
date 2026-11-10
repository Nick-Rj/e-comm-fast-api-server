# Database Infrastructure: Create the asynchronous database engine and a reusable session factory.
# This implementation follows SQLAlchemy's recommended asynchronous engine and session-factory pattern.

# from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

from sqlmodel.ext.asyncio.session import AsyncSession

from .config import settings

# --------------------------------------
# DATABASE ENGINE
# --------------------------------------

# Create the asynchronous database engine.
# The engine manages database connectivity and the connection pool.
# Connections are established when required, not all at startup.
engine = create_async_engine(
    settings.DATABASE_URL.get_secret_value(), 
    echo = True, # Log SQL statements (only for development env).
    pool_pre_ping = True # Check pooled connections before using them.
)

# --------------------------------------
# ASYNC SESSION FACTORY
# --------------------------------------


# Creating async session for managing the pool of DB connections.
# It creates a reusable factory for asynchronous database sessions.
# Each task/call like create, update, etc., to this factory produces a new AsyncSession.
# SQLAlchemy 2.x provides a dedicated async_sessionmaker specially for asynchronous sessions.
AsyncSessionFactory = async_sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit = False
)

# --------------------------------------
# DATABASE SESSION DEPENDENCY
#---------------------------------------

# Generating sessions from Session Factory
async def get_session():
    """
    Provides a database session to FastAPI endpoints.

    Each request gets its own session.
    The session is automatically closed after use.

    CRUD functions currently own transaction commits.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except:
            # Rollback any failed or uncommitted transaction.
            await session.rollback()
            raise