from fastapi import FastAPI
from app.db.database import engine
from app.db.models.base import Base

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Knowledge Base API",
    description="RAG-powered knowledge base API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to AI Knowledge Base API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
