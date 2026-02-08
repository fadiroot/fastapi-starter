"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from src.api.routes import user_routes
from src.application.exceptions.application_exceptions import ApplicationException
from src.domain.exceptions.domain_exceptions import DomainException
from src.infrastructure.config.settings import get_settings
from src.infrastructure.database.postgresql.connection import PostgreSQLConnection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan: connect DB on startup, disconnect on shutdown."""
    settings = get_settings()
    db = PostgreSQLConnection(settings)
    await db.connect()
    app.state.db = db

    # Create users table if not exists (for development)
    factory = db.session_factory()
    async with factory() as session:
        await session.execute(
            text("""
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
        )
        await session.commit()

    yield

    await db.disconnect()


app = FastAPI(
    title="FastAPI Clean Architecture Starter",
    description="Python starter with Clean Architecture, FastAPI, and PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routers with prefix
settings = get_settings()
app.include_router(user_routes.router, prefix=settings.api_v1_prefix)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


# Exception handlers for domain/application exceptions
@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    """Handle domain exceptions."""
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message, "code": exc.code},
    )


@app.exception_handler(ApplicationException)
async def application_exception_handler(
    request: Request, exc: ApplicationException
) -> JSONResponse:
    """Handle application exceptions."""
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message, "code": exc.code},
    )
