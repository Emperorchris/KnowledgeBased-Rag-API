from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import api_router
from .core.exceptions import register_exception_handlers
from app.db.database import engine
from app.db.models.base import Base

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Knowledge Base API",
    description="RAG-powered knowledge base API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.router.include_router(api_router, prefix="/api/v1")  # Include API routes from router.py

# Register exception handlers
register_exception_handlers(app)

@app.get("/")
def root():
    return {"message": "Welcome to AI Knowledge Base API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
