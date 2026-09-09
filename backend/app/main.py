"""FastAPI application entry point with CORS middleware and router inclusion."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from .config import get_settings
from .database import init_db
from .routers import auth_router, transaction_router, analytics_router, wealth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="FinTech Behavioral Guidance Platform API", lifespan=lifespan)

# CORS — explicit origins list is required when allow_credentials=True.
# For local development we allow both localhost variants.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler — returns JSON instead of crashing with HTML
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )


# Include routers
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(transaction_router.router, prefix="/transactions", tags=["transactions"])
app.include_router(analytics_router.router, prefix="/analytics", tags=["analytics"])
app.include_router(wealth_router.router, prefix="/wealth", tags=["wealth"])


@app.get("/health", summary="Health check")
async def health_check():
    return {"status": "ok"}
