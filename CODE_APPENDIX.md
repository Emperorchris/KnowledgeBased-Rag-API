# CODE APPENDIX — AI Knowledge Base API

## File Index

| # | File Path | Lines | Description |
|---|-----------|-------|-------------|
| 1 | `app/main.py` | 38 | FastAPI application entry point with CORS middleware and route registration |
| 2 | `app/__init__.py` | 1 | Empty package initialiser for the app module |
| 3 | `app/core/config.py` | 48 | Centralised configuration loading from environment variables |
| 4 | `app/core/__init__.py` | 61 | Core package exports for config, exceptions, logger, and security |
| 5 | `app/core/dependencies.py` | 29 | FastAPI dependency injection for DB sessions and authenticated users |
| 6 | `app/core/exceptions.py` | 117 | Custom HTTP exception classes and global exception handlers |
| 7 | `app/core/logger.py` | 29 | Logger factory with console and file output handlers |
| 8 | `app/core/security.py` | 44 | Password hashing (Argon2), JWT token creation/verification, refresh token generation |
| 9 | `app/db/__init__.py` | 8 | Database package exports for engine, session, and all models |
| 10 | `app/db/database.py` | 25 | SQLAlchemy engine and session factory for MySQL via PyMySQL |
| 11 | `app/db/create_tables.py` | 11 | Utility script to create all database tables from SQLAlchemy models |
| 12 | `app/db/models/__init__.py` | 34 | Models package aggregating all ORM model imports |
| 13 | `app/db/models/base.py` | 9 | Shared SQLAlchemy declarative base for all models |
| 14 | `app/db/models/enums.py` | 14 | Enum definitions for document sources and message roles |
| 15 | `app/db/models/user.py` | 42 | User ORM model with email and name validation |
| 16 | `app/db/models/chat.py` | 154 | ChatSession and Message ORM models with relationships and validators |
| 17 | `app/db/models/document.py` | 124 | Document and DocumentChunk ORM models for uploaded files and their vector chunks |
| 18 | `app/db/models/refresh_token.py` | 26 | RefreshToken ORM model for JWT refresh token persistence |
| 19 | `app/db/models/api_logs.py` | 104 | APILog and DailyStatistics ORM models for monitoring and analytics |
| 20 | `app/db/models/cache.py` | 37 | EmbeddingCache ORM model for caching OpenAI embedding responses |
| 21 | `app/db/models/events.py` | 21 | SQLAlchemy event listeners for automatic timestamp updates (currently disabled) |
| 22 | `app/ai/rag/__init__.py` | 1 | Empty package initialiser for the RAG module |
| 23 | `app/ai/rag/chunker.py` | 23 | Document chunking by title structure and recursive text splitting |
| 24 | `app/ai/rag/doc_partition.py` | 62 | Document partitioning using Unstructured library (text, tables, images) |
| 25 | `app/ai/rag/embedder.py` | 38 | OpenAI embedding generation with database-backed caching |
| 26 | `app/ai/rag/enhance_content.py` | 84 | LLM-powered image description and table summarisation for document enrichment |
| 27 | `app/ai/rag/ingestion.py` | 64 | End-to-end document ingestion pipeline (partition → enrich → chunk → store) |
| 28 | `app/ai/rag/retrieval.py` | 101 | RAG retrieval: vector similarity search, context building, and LLM answer generation |
| 29 | `app/ai/rag/vector_store.py` | 11 | ChromaDB vector store initialisation with OpenAI embeddings |
| 30 | `app/api/__init__.py` | 3 | API package export for the aggregated router |
| 31 | `app/api/router.py` | 8 | Central API router that includes auth, document, and chat sub-routers |
| 32 | `app/api/endpoints/__init__.py` | 3 | Endpoints package export for all route modules |
| 33 | `app/api/endpoints/auth.py` | 25 | Auth API routes: register, login, refresh, revoke, logout |
| 34 | `app/api/endpoints/chat.py` | 24 | Chat API routes: send message, get history, list sessions |
| 35 | `app/api/endpoints/document.py` | 68 | Document API routes: upload, list, get, download, delete |
| 36 | `app/modules/__init__.py` | 15 | Modules package export for auth service functions |
| 37 | `app/modules/auth_service.py` | 133 | Authentication business logic: register, login, token rotation, logout |
| 38 | `app/modules/chat_service.py` | 294 | Chat business logic: session management, RAG-powered Q&A, cost tracking |
| 39 | `app/modules/document_service.py` | 157 | Document business logic: file upload, ingestion orchestration, deletion |
| 40 | `app/modules/user_service.py` | 1 | Empty placeholder for future user service logic |
| 41 | `app/schemas/__init__.py` | 21 | Schemas package export for all Pydantic request/response models |
| 42 | `app/schemas/user.py` | 44 | Pydantic schemas for user registration, login, and auth responses |
| 43 | `app/schemas/chat.py` | 102 | Pydantic schemas for chat requests, responses, and source references |
| 44 | `app/schemas/document.py` | 61 | Pydantic schemas for document CRUD and chunk responses |
| 45 | `app/schemas/refresh_token.py` | 12 | Pydantic schema for refresh token responses |
| 46 | `alembic/env.py` | 83 | Alembic migration environment configuration |
| 47 | `alembic/versions/587dd353c1e3_add_total_tables_and_images.py` | 35 | Migration: add total_tables and total_images columns to documents table |

**Total line count: 2,449 lines across 47 files**

---

## 1. `app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import api_router
from .core.exceptions import register_exception_handlers
from app.db.database import engine
from app.db.models.base import Base

# Create all tables
# Base.metadata.create_all(bind=engine)

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
```

---

## 2. `app/__init__.py`

```python
```

---

## 3. `app/core/config.py`

```python
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

SECRET_KEY = os.getenv("SECRET_KEY", "<REDACTED>")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
LARGE_LANGUAGE_MODEL = os.getenv("LARGE_LANGUAGE_MODEL", "gpt-5.4-nano")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

INPUT_COST_PER_MILLION = float(os.getenv("INPUT_COST_PER_MILLION", 2.50))
OUTPUT_COST_PER_MILLION = float(os.getenv("OUTPUT_COST_PER_MILLION", 10.00))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOADED_FILES_DIR = os.getenv("UPLOADED_FILES_DIR", os.path.join(BASE_DIR, "uploaded_doc_files"))
CHROMA_PERSISTENCE_DIR = os.getenv("CHROMA_PERSISTENCE_DIR", os.path.join(BASE_DIR, "chroma_db"))

API_RATE_LIMIT_PER_MINUTE = int(os.getenv("API_RATE_LIMIT_PER_MINUTE", "60"))

COMPANY_NAME = os.getenv("COMPANY_NAME", "Sonichoice Logistics Serivices")
COMPANY_EMAIL = os.getenv("SUPPORT_EMAIL", "info@sonichoicelogistics.com")
COMPANY_WEBSITE = os.getenv("COMPANY_WEBSITE", "https://www.inventory.sonichoicelogistics.com")

AI_NAME = os.getenv("AI_NAME", "SonicAI")
AI_DESCRIPTION = os.getenv("AI_DESCRIPTION", f"{AI_NAME} is a powerful knowledge-based assistant designed to help you quickly find answers and insights from {COMPANY_NAME}.")
# if not all([MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, OPENAI_API_KEY]):
#     raise Exception("Missing environment variables")

required_vars = ["MYSQL_HOST", "MYSQL_PORT", "MYSQL_USER", "MYSQL_DATABASE", "OPENAI_API_KEY"]
missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    raise Exception(f"Missing environment variables: {', '.join(missing)}")
```

---

## 4. `app/core/__init__.py`

```python
from .config import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DATABASE,
    ANTHROPIC_API_KEY,
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    LARGE_LANGUAGE_MODEL,
    MAX_TOKENS,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    API_RATE_LIMIT_PER_MINUTE,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
)

from .exceptions import (
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
    ConflictException,
    InternalServerException,
    register_exception_handlers,
)

from .logger import get_logger
from .security import hash_password, verify_password, create_access_token, verify_access_token, generate_refresh_token
__all__ = [
    "MYSQL_HOST",
    "MYSQL_PORT",
    "MYSQL_USER",
    "MYSQL_PASSWORD",
    "MYSQL_DATABASE",
    "ANTHROPIC_API_KEY",
    "OPENAI_API_KEY",
    "EMBEDDING_MODEL",
    "LARGE_LANGUAGE_MODEL",
    "MAX_TOKENS",
    "CHUNK_SIZE",
    "CHUNK_OVERLAP",
    "API_RATE_LIMIT_PER_MINUTE",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "ALGORITHM",
    "NotFoundException",
    "BadRequestException",
    "UnauthorizedException",
    "ForbiddenException",
    "ConflictException",
    "InternalServerException",
    "register_exception_handlers",
    "get_logger",
    "hash_password",
    "verify_password",
    "create_access_token",
    "verify_access_token",
    "generate_refresh_token",
]
```

---

## 5. `app/core/dependencies.py`

```python
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..core.security import verify_access_token
from ..core.config import SECRET_KEY, ALGORITHM
from ..core.exceptions import NotFoundException, UnauthorizedException
from ..db.database import get_db
from ..db.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

DB = Annotated[Session, Depends(get_db)]
Token = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(token: Token, db: DB) -> User:
    payload = verify_access_token(token, SECRET_KEY, [ALGORITHM])
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token", error_detail={"reason": "Token payload missing user ID"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("User not found", error_detail={"user_id": str(user_id)})
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
```

---

## 6. `app/core/exceptions.py`

```python
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import traceback


# Custom exceptions
class NotFoundException(HTTPException):
    def __init__(self, error_message: str = "Resource not found", error_detail=None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=error_message)
        self.error_detail = error_detail

    def to_dict(self):
        return {"message": self.detail, "error_detail": self.error_detail}

class BadRequestException(HTTPException):
    def __init__(self, error_message: str = "Bad request", error_detail=None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)
        self.error_detail = error_detail

    def to_dict(self):
        return {"message": self.detail, "error_detail": self.error_detail}


class UnauthorizedException(HTTPException):
    def __init__(self, error_message: str = "Unauthorized", error_detail=None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_message,
            headers={"WWW-Authenticate": "Bearer"},
        )
        self.error_detail = error_detail

    def to_dict(self):
        return {"message": self.detail, "error_detail": self.error_detail}


class ForbiddenException(HTTPException):
    def __init__(self, error_message: str = "Forbidden", error_detail=None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=error_message)
        self.error_detail = error_detail

    def to_dict(self):
        return {"message": self.detail, "error_detail": self.error_detail}


class ConflictException(HTTPException):
    def __init__(self, error_message: str = "Resource already exists", error_detail=None):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=error_message)
        self.error_detail = error_detail

    def to_dict(self):
        return {"message": self.detail, "error_detail": self.error_detail}

class InternalServerException(HTTPException):
    def __init__(self, error_message: str = "Internal server error", error_detail=None):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
        self.error_detail = error_detail

    def to_dict(self):
        return {"message": self.detail, "error_detail": self.error_detail}

# Register exception handlers on the app
def register_exception_handlers(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            errors.append({
                "field": " -> ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            })
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "Validation error", "errors": errors},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        tb = traceback.format_exc()
        print(f"HTTP error: {exc.status_code} - {exc.detail}\n{tb}")
        if hasattr(exc, "to_dict"):
            content = exc.to_dict()
        else:
            content = {
                "message": exc.detail,
                "error_detail": {
                    "status_code": exc.status_code,
                    "error_type": type(exc).__name__,
                    "method": request.method,
                    "url": str(request.url),
                    "content_type": request.headers.get("content-type", "unknown"),
                    "hint": "If uploading files, use multipart/form-data, not application/json",
                },
            }
        return JSONResponse(
            status_code=exc.status_code,
            content=content,
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        tb = traceback.format_exc()
        print(f"Unhandled error: {type(exc).__name__}: {exc}\n{tb}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=InternalServerException(
                error_detail={
                    "error_type": type(exc).__name__,
                    "cause": str(exc),
                    "stack_trace": tb.splitlines(),
                }
            ).to_dict(),
        )
```

---

## 7. `app/core/logger.py`

```python
import logging
import sys


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File output
        file_handler = logging.FileHandler("app.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
```

---

## 8. `app/core/security.py`

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
from jwt.exceptions import PyJWTError, InvalidTokenError
from datetime import datetime, timedelta, timezone
import secrets
from typing import Optional
from .config import SECRET_KEY, ALGORITHM

from .exceptions import UnauthorizedException

def hash_password(password: str) -> str:
    return PasswordHasher().hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    try:
        PasswordHasher().verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None, secret_key: str = SECRET_KEY, algorithm: str = ALGORITHM) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def verify_access_token(token: str, secret_key: str = SECRET_KEY, algorithms: list = [ALGORITHM]) -> Optional[dict]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithms)
        return payload
    except (InvalidTokenError, PyJWTError):
        raise UnauthorizedException("Invalid or expired token", error_detail={"reason": "Token could not be decoded or has expired"})

    return None


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)
```

---

## 9. `app/db/__init__.py`

```python
from .database import engine, get_db
from .models import Base, Document, DocumentChunk, ChatSession, Message, APILog, DailyStatistics, EmbeddingCache, User


__all__ = [
    "database",
    "models",
]
```

---

## 10. `app/db/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE



SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 11. `app/db/create_tables.py`

```python
from .database import engine
from .models.base import Base
from .models import User, Document, DocumentChunk, ChatSession, Message, APILog, DailyStatistics, EmbeddingCache  # noqa: F401
from .models.refresh_token import RefreshToken  # noqa: F401

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()
```

---

## 12. `app/db/models/__init__.py`

```python
"""
Models package - import everything from here.

Usage:
    from app.db.models import Base, Document, ChatSession, Message
"""

from .base import Base
from .enums import DocumentSourceEnum, MessageRoleEnum
from .document import Document, DocumentChunk
from .chat import ChatSession, Message
from .api_logs import APILog, DailyStatistics
from .cache import EmbeddingCache
from .user import User
from .refresh_token import RefreshToken

# Register event listeners
from . import events  # noqa: F401

__all__ = [
    "Base",
    "DocumentSourceEnum",
    "MessageRoleEnum",
    "Document",
    "DocumentChunk",
    "ChatSession",
    "Message",
    "APILog",
    "DailyStatistics",
    "EmbeddingCache",
    "User",
    "RefreshToken",
]
```

---

## 13. `app/db/models/base.py`

```python
"""
Shared base for all SQLAlchemy models.
Every model file imports Base from here so they all share the same metadata.
"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```

---

## 14. `app/db/models/enums.py`

```python
import enum

class DocumentSourceEnum(str, enum.Enum):
    UPLOADED = "uploaded"
    IMPORTED = "imported"
    GENERATED = "generated"
    SCRAPED = "scraped"


class MessageRoleEnum(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
```

---

## 15. `app/db/models/user.py`

```python
from .base import Base
from sqlalchemy import Column, String, Integer, Text, DateTime, Float, Boolean, ForeignKey, JSON, Uuid
from sqlalchemy.orm import validates
import uuid
from datetime import datetime, timezone
from email_validator import validate_email, EmailNotValidError

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


    @validates("name")
    def validate_name(self, key, value):
        value = value.strip() if value else value
        if not value:
            raise ValueError("Name cannot be empty")
        if len(value) > 255:
            raise ValueError("Name must be <= 255 characters")
        return value

    @validates("email")
    def validate_email_field(self, key, value):
        value = value.strip().lower() if value else value
        if not value:
            raise ValueError("Email cannot be empty")
        if len(value) > 255:
            raise ValueError("Email must be <= 255 characters")
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValueError("Please provide a valid email address")
        return value
```

---

## 16. `app/db/models/chat.py`

```python
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Integer, Text, DateTime, Float, Boolean,
    ForeignKey, Index, Enum as SQLEnum, JSON, Uuid,
)
from sqlalchemy.orm import relationship, validates
import uuid

from .base import Base
from .enums import MessageRoleEnum


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    __table_args__ = (
        Index("ix_chat_sessions_user_id", "user_id"),
        Index("ix_chat_sessions_created_at", "created_at"),
    )

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    user_id = Column(Uuid, nullable=True)
    document_ids = Column(JSON, nullable=True, default=list)
    total_messages = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    archived_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    messages = relationship(
        "Message",
        back_populates="session",
        cascade="all, delete-orphan",
        foreign_keys="Message.session_id",
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value) == 0:
            raise ValueError("Session name cannot be empty")
        if len(value) > 255:
            raise ValueError("Session name must be <= 255 characters")
        return value

    @property
    def message_count(self) -> int:
        return len(self.messages) if self.messages else 0

    @property
    def is_archived(self) -> bool:
        return self.archived_at is not None

    def __repr__(self):
        return f"<ChatSession id={self.id} name={self.name} messages={self.total_messages}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "user_id": self.user_id,
            "document_ids": self.document_ids or [],
            "total_messages": self.total_messages,
            "total_tokens": self.total_tokens,
            "total_cost": round(self.total_cost, 4),
            "is_active": self.is_active,
            "is_archived": self.is_archived,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (
        Index("ix_messages_session_id", "session_id"),
        Index("ix_messages_role", "role"),
        Index("ix_messages_created_at", "created_at"),
    )

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, unique=True, index=True)
    session_id = Column(
        Uuid,
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    document_id = Column(
        Uuid,
        ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True,
    )
    role = Column(SQLEnum(MessageRoleEnum, native_enum=False), nullable=False, default=MessageRoleEnum.USER.value)
    content = Column(Text, nullable=False)
    document_ids_used = Column(JSON, nullable=True, default=list)
    relevance_scores = Column(JSON, nullable=True, default=dict)
    retrieved_chunk_count = Column(Integer, nullable=True)
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    estimated_cost = Column(Float, default=0.0)
    user_rating = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    session = relationship("ChatSession", back_populates="messages")
    document = relationship("Document", back_populates="messages")

    @validates("role")
    def validate_role(self, key, value):
        if isinstance(value, str):
            valid_roles = ["user", "assistant", "system"]
            if value.lower() not in valid_roles:
                raise ValueError(f"Role must be one of: {valid_roles}")
        return value

    @validates("user_rating")
    def validate_rating(self, key, value):
        if value is not None and (value < 1 or value > 5):
            raise ValueError("Rating must be between 1 and 5")
        return value

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def is_assistant(self) -> bool:
        return self.role == MessageRoleEnum.ASSISTANT.value or self.role == "assistant"

    @property
    def is_user(self) -> bool:
        return self.role == MessageRoleEnum.USER.value or self.role == "user"

    def __repr__(self):
        return f"<Message id={self.id} role={self.role} tokens={self.total_tokens}>"

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "role": self.role,
            "content": self.content[:200] + "..." if len(self.content) > 200 else self.content,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "estimated_cost": round(self.estimated_cost, 6),
            "user_rating": self.user_rating,
            "created_at": self.created_at.isoformat(),
        }
```

---

## 17. `app/db/models/document.py`

```python
from datetime import datetime, timedelta, timezone
from sqlalchemy import (
    Column, String, Integer, Text, DateTime, Float, Boolean,
    ForeignKey, Index, Enum, JSON, Uuid,
)
from sqlalchemy.orm import relationship, validates
import uuid

from .base import Base
from .enums import DocumentSourceEnum


class Document(Base):
    __tablename__ = "documents"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    file_location = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    file_type = Column(String(10), nullable=False)
    size_bytes = Column(Integer, nullable=False)
    content = Column(Text, nullable=True)
    source = Column(
        Enum(DocumentSourceEnum, native_enum=False),
        default=DocumentSourceEnum.UPLOADED,
        nullable=False,
    )
    tags = Column(JSON, nullable=True, default=list)
    extra_metadata = Column(JSON, nullable=True, default=dict)
    author = Column(String(255), nullable=True)
    chunks = Column(Integer, default=0)
    tokens = Column(Integer, default=0)
    total_tables = Column(Integer, default=0)
    total_images = Column(Integer, default=0)
    chunk_ids = Column(JSON, nullable=True, default=list)
    is_processed = Column(Boolean, default=False)
    relevance_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    messages = relationship(
        "Message",
        back_populates="document",
        cascade="all, delete-orphan",
        foreign_keys="Message.document_id",
    )
    chunks_rel = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value) == 0:
            raise ValueError("Document name cannot be empty")
        if len(value) > 255:
            raise ValueError("Document name must be <= 255 characters")
        return value

    @validates("file_type")
    def validate_file_type(self, key, value):
        allowed = [".txt", ".pdf", ".md", ".docx", ".html", ".json"]
        if value.lower() not in allowed:
            raise ValueError(f"File type must be one of: {allowed}")
        return value.lower()

    @property
    def size_mb(self) -> float:
        return round(self.size_bytes / (1024 * 1024), 2)

    @property
    def is_large(self) -> bool:
        return self.size_mb > 100

    def __repr__(self):
        return f"<Document id={self.id} name={self.name} chunks={self.chunks}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "file_type": self.file_type,
            "size_bytes": self.size_bytes,
            "size_mb": self.size_mb,
            "source": self.source.value,
            "chunks": self.chunks,
            "tokens": self.tokens,
            "author": self.author,
            "is_processed": self.is_processed,
            "relevance_score": self.relevance_score,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "total_tables": self.total_tables,
            "total_images": self.total_images,
        }


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    __table_args__ = (
        Index("ix_document_chunks_document_id", "document_id"),
        Index("ix_document_chunks_vector_id", "vector_id"),
    )

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, unique=True, index=True)
    document_id = Column(
        Uuid,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    tokens = Column(Integer, default=0)
    vector_id = Column(String(255), nullable=True, unique=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    document = relationship("Document", back_populates="chunks_rel")

    def __repr__(self):
        return f"<DocumentChunk doc={self.document_id} index={self.chunk_index}>"
```

---

## 18. `app/db/models/refresh_token.py`

```python
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Uuid, ForeignKey

from .base import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, unique=True, index=True)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<RefreshToken id={self.id} user_id={self.user_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "token": self.token,
            "created_at": self.created_at.isoformat(),
        }
```

---

## 19. `app/db/models/api_logs.py`

```python
"""
APILog and DailyStatistics models for monitoring and analytics.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Integer, Text, DateTime, Float, Uuid,
    Index, UniqueConstraint,
)
from sqlalchemy.orm import validates
import uuid

from .base import Base


class APILog(Base):
    """
    API request logging for monitoring and debugging.
    """

    __tablename__ = "api_logs"
    __table_args__ = (
        Index("ix_api_logs_endpoint", "endpoint"),
        Index("ix_api_logs_status_code", "status_code"),
        Index("ix_api_logs_created_at", "created_at"),
    )

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, unique=True, index=True)

    # Request Information
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    user_id = Column(String(100), nullable=True)

    # Response Information
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Integer, nullable=False)
    error_message = Column(Text, nullable=True)

    # Usage Information
    tokens_used = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)

    # Request Details
    request_size_bytes = Column(Integer, nullable=True)
    response_size_bytes = Column(Integer, nullable=True)

    # Timestamp
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<APILog endpoint={self.endpoint} status={self.status_code} time={self.response_time_ms}ms>"

    def to_dict(self):
        return {
            "id": self.id,
            "endpoint": self.endpoint,
            "method": self.method,
            "status_code": self.status_code,
            "response_time_ms": self.response_time_ms,
            "tokens_used": self.tokens_used,
            "cost": round(self.cost, 6) if self.cost else None,
            "created_at": self.created_at.isoformat(),
        }


class DailyStatistics(Base):
    """
    Daily aggregated statistics for monitoring dashboards.
    """

    __tablename__ = "daily_statistics"
    __table_args__ = (
        Index("ix_daily_statistics_date", "date"),
        UniqueConstraint("date", name="uq_daily_statistics_date"),
    )

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, unique=True, index=True)
    date = Column(String(10), nullable=False, unique=True)

    # Counts
    documents_uploaded = Column(Integer, default=0)
    documents_deleted = Column(Integer, default=0)
    sessions_created = Column(Integer, default=0)
    messages_sent = Column(Integer, default=0)
    api_calls = Column(Integer, default=0)

    # Token Usage
    total_input_tokens = Column(Integer, default=0)
    total_output_tokens = Column(Integer, default=0)

    # Cost
    total_cost = Column(Float, default=0.0)

    # Performance
    average_response_time_ms = Column(Float, default=0.0)
    error_count = Column(Integer, default=0)

    # Timestamp
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<DailyStatistics date={self.date} messages={self.messages_sent} cost=${self.total_cost:.2f}>"
```

---

## 20. `app/db/models/cache.py`

```python
"""
EmbeddingCache model for avoiding redundant embedding API calls.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Integer, DateTime, JSON,
    Index, UniqueConstraint,
)
import uuid

from .base import Base


class EmbeddingCache(Base):
    """
    Cache for embeddings to avoid re-embedding the same text.
    """

    __tablename__ = "embedding_cache"
    __table_args__ = (
        Index("ix_embedding_cache_text_hash", "text_hash"),
        UniqueConstraint("text_hash", name="uq_embedding_cache_hash"),
    )

    id = Column(String(50), primary_key=True, default=lambda: f"emb_{uuid.uuid4().hex[:12]}")
    text_hash = Column(String(64), nullable=False, unique=True)
    text_snippet = Column(String(500), nullable=False)
    embedding = Column(JSON, nullable=False)
    embedding_model = Column(String(50), default="text-embedding-3-small")
    hit_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_accessed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<EmbeddingCache hash={self.text_hash[:8]} hits={self.hit_count}>"
```

---

## 21. `app/db/models/events.py`

```python
# """
# SQLAlchemy event listeners for automatic timestamp updates.
# Import this module once at app startup to register the listeners.
# """

# from datetime import datetime, timezone
# from sqlalchemy import event

# from .document import Document
# from .chat import ChatSession


# @event.listens_for(ChatSession, "before_update")
# def update_chat_session_timestamp(mapper, connection, target):
#     target.updated_at = datetime.now(timezone.utc)


# @event.listens_for(Document, "before_update")
# def update_document_timestamp(mapper, connection, target):
#     target.updated_at = datetime.now(timezone.utc)
```

---

## 22. `app/ai/rag/__init__.py`

```python
```

---

## 23. `app/ai/rag/chunker.py`

```python
from unstructured.chunking.title import chunk_by_title
from ...core.config import CHUNK_OVERLAP, CHUNK_SIZE
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_document_by_title(elements, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Chunks a document based on its title structure using the unstructured library's chunk_by_title function.
    This method preserves the logical structure of the document by using titles as natural breakpoints.
    """
    chunks = chunk_by_title(
        elements,
        chunk_size=chunk_size,
        overlap=overlap,
        combine_text_under_n_chars=500,
        new_after_n_chars=chunk_size + 800 # Fallback to chunking after a certain number of characters if no titles are found within that range
    )
    return chunks


def chunk_document_by_recursive_splitter(text, metadata=None, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.create_documents([text], metadatas=[metadata] if metadata else None)
```

---

## 24. `app/ai/rag/doc_partition.py`

```python
from unstructured.partition.auto import partition, PartitionStrategy
from unstructured.documents.elements import Table, Image
from io import BytesIO


SUPPORTED_FILE_TYPES = ["txt", "pdf", "md", "docx", "html", "json"]


def partition_document(file_bytes: bytes, filename: str) -> dict:
    file_type = filename.rsplit(".", 1)[-1].lower()

    if file_type not in SUPPORTED_FILE_TYPES:
        raise ValueError(f"Unsupported file type: {file_type}. Supported: {SUPPORTED_FILE_TYPES}")

    elements = partition(
        file=BytesIO(file_bytes),
        metadata_filename=filename,
        infer_table_structure=True,
        strategy=PartitionStrategy.HI_RES,
        extract_image_block_to_payload=True,
        extract_image_block_types=["Image", "Table"],
        skip_infer_table_types=[],
    )


    if not elements:
        raise ValueError("No content could be extracted from the file")

    text_elements = []
    tables = []
    images = []

    print(f"--- Proccessed elemnts: {elements} ---")

    for el in elements:
        if isinstance(el, Table):
            tables.append({
                "content": str(el),
                "html": el.metadata.text_as_html if hasattr(el.metadata, "text_as_html") else None,
                "page": el.metadata.page_number,
            })
        elif isinstance(el, Image):
            images.append({
                "content": str(el),
                "image_base64": el.metadata.image_base64 if hasattr(el.metadata, "image_base64") else None,
                "page": el.metadata.page_number,
            })
        else:
            text_elements.append(str(el))

    full_text = "\n\n".join(text_elements)

    return {
        "text": full_text,
        "elements": elements,
        "tables": tables,
        "images": images,
        "element_count": len(elements),
        "table_count": len(tables),
        "image_count": len(images),
    }
```

---

## 25. `app/ai/rag/embedder.py`

```python
from langchain_openai import OpenAIEmbeddings
from ...core.config import OPENAI_API_KEY, EMBEDDING_MODEL
from ...db.models import EmbeddingCache
from sqlalchemy.orm import Session
import hashlib

embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL, api_key=OPENAI_API_KEY)

def get_embedding_model() -> OpenAIEmbeddings:
    return embedding_model


def embed_query(text: str) -> list[float]:
    return embedding_model.embed_query(text)


def embed_documents(texts: list[str]) -> list[list[float]]:
    return embedding_model.embed_documents(texts)

def embed_with_cache(text: str, db: Session) -> list[float]:
    text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
    cache_entry = db.query(EmbeddingCache).filter_by(text_hash=text_hash).first()
    if cache_entry:
        cache_entry.hit_count += 1
        db.commit()
        return cache_entry.embedding
    else:
        embedding = embed_query(text)
        new_cache_entry = EmbeddingCache(
            text_hash=text_hash,
            text_snippet=text[:500],
            embedding=embedding,
            embedding_model=EMBEDDING_MODEL,
        )
        db.add(new_cache_entry)
        db.commit()
        return embedding
```

---

## 26. `app/ai/rag/enhance_content.py`

```python
from langchain_openai import ChatOpenAI, OpenAI
from ...core.config import OPENAI_API_KEY, LARGE_LANGUAGE_MODEL
import imghdr
import base64

llm = ChatOpenAI(
    model=LARGE_LANGUAGE_MODEL,
    api_key=OPENAI_API_KEY,
    temperature=0,
)


def get_image_type(image_base64: str) -> str:
    image_bytes = base64.b64decode(image_base64)
    image_type = imghdr.what(None, h=image_bytes)
    ext = image_type if image_type else "png"  # default to png if type can't be determined
    return f"image/{ext}"


def describe_image(image_base64: str, context: str = "") -> str:
    prompt = (
        "You are analyzing an image extracted from a document.\n\n"
        "Provide:\n"
        "1. What type of image this is (photo, chart, diagram, screenshot, logo, etc.)\n"
        "2. All visible text, labels, numbers, and annotations\n"
        "3. If it's a chart/graph: the axes, data points, trends, and comparisons\n"
        "4. If it's a diagram/flowchart: the components, connections, and flow\n"
        "5. If it's a photo/screenshot: the key subjects and relevant details\n\n"
        "Be factual and thorough. Only describe what is visible in the image."
    )

    if context:
        prompt += f"\n\nDocument context: {context}"

    image_type = get_image_type(image_base64)
    response = llm.invoke([
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{image_type};base64,{image_base64}"},
                },
            ],
        }
    ])
    return response.content


def summarize_table(table_content: str, table_html: str = None) -> str:
    table_data = table_html if table_html else table_content
    prompt = (
        "You are analyzing a table extracted from a document.\n\n"
        f"Table data:\n{table_data}\n\n"
        "Provide:\n"
        "1. What this table represents\n"
        "2. Column and row descriptions\n"
        "3. Key data points, trends, or comparisons\n"
        "4. Any notable outliers or patterns\n\n"
        "Be factual. Only describe what is in the table."
    )

    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content


def enrich_partitioned_document(partitioned: dict) -> dict:
    enriched_text_parts = [partitioned["text"]]

    for i, table in enumerate(partitioned["tables"]):
        summary = summarize_table(table["content"], table.get("html"))
        table["summary"] = summary
        enriched_text_parts.append(f"[Table {i + 1}, Page {table.get('page', '?')}]: {summary}")

    for i, image in enumerate(partitioned["images"]):
        if image.get("image_base64"):
            description = describe_image(image["image_base64"])
            image["description"] = description
            enriched_text_parts.append(f"[Image {i + 1}, Page {image.get('page', '?')}]: {description}")

    partitioned["enriched_text"] = "\n\n".join(enriched_text_parts)
    return partitioned
```

---

## 27. `app/ai/rag/ingestion.py`

```python
from .enhance_content import enrich_partitioned_document
from .chunker import  chunk_document_by_recursive_splitter
from .vector_store import vector_store
from .doc_partition import partition_document
from datetime import datetime, timezone


def ingestion_pipeline(file_bytes: bytes, filename: str, document_id: str, tags: str = "") -> dict:
    """
    Main pipeline for ingesting a document into the knowledge base.
    Steps:
    1. Partition document into elements (text, tables, images)
    2. Enrich content (describe images, summarize tables)
    3. Chunk elements by title structure
    4. Append enriched descriptions to chunk texts
    5. Store in vector database (Chroma auto-embeds)
    """

    print("Ingesting document...")
    file_type = filename.rsplit(".", 1)[-1].lower()

    print("Partitioning document...")
    partitioned = partition_document(file_bytes, filename)

    print("Enriching document content...")
    enriched = enrich_partitioned_document(partitioned)

    print("Chunking document...")

    chunks = chunk_document_by_recursive_splitter(
        enriched["enriched_text"],
        metadata={
            "document_id": document_id,
            "filename": filename,
            "source": "uploaded",
            "upload_date": datetime.now(timezone.utc).isoformat(),
            "file_type": file_type,
            "tags": tags or "",
        },
    )

    # Set chunk_index per chunk
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i

    print("Storing document chunks in vector store...")
    ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
    vector_store.add_documents(chunks, ids=ids)

    print("Document ingested successfully!")
    return {
        "document_id": document_id,
        "chunk_ids": ids,
        "chunk_texts": [chunk.page_content for chunk in chunks],
        "filename": filename,
        "chunk_count": len(chunks),
        "enriched_text": enriched["enriched_text"],
        "is_enriched": enriched["enriched_text"] != partitioned["text"],
        "text_count": len(partitioned["text"] or []),
        "table_count": len(partitioned["tables"] or []),
        "image_count": len(partitioned["images"] or []),
    }
```

---

## 28. `app/ai/rag/retrieval.py`

```python
from langchain_openai import ChatOpenAI
from .vector_store import vector_store
from ...core.config import OPENAI_API_KEY, LARGE_LANGUAGE_MODEL


llm = ChatOpenAI(
    model=LARGE_LANGUAGE_MODEL,
    api_key=OPENAI_API_KEY,
    temperature=0,
)


def retrieve_relevant_chunks(query: str, k: int = 5, filter: dict = None) -> list[dict]:
    results = vector_store.similarity_search_with_score(
        query=query,
        k=k,
        filter=filter,
    )
    print(f"Retrieved {len(results)} relevant chunks for query: '{query}'")

    return [
        {
            "content": doc.page_content,
            "metadata": doc.metadata,
            "score": score,
        }
        for doc, score in results
    ]


def build_context(chunks: list[dict]) -> str:
    context_parts = []
    for i, chunk in enumerate(chunks):
        source = chunk["metadata"].get("document_id", "unknown")
        context_parts.append(f"[Source {i + 1} - Document: {source}]\n{chunk['content']}")
    return "\n\n---\n\n".join(context_parts)


def generate_answer(query: str, context: str) -> str:
    prompt = (
        "You are a helpful assistant that answers questions based on the provided context.\n"
        "Only use the information from the context below. If the answer is not in the context, "
        "say \"I don't have enough information to answer that question.\"\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}"
    )

    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content


def query_knowledge_base(query: str, k: int = 5, filter: dict = None) -> dict:
    chunks = retrieve_relevant_chunks(query, k=k, filter=filter)

    if not chunks:
        return {
            "answer": "No relevant documents found for your question.",
            "sources": [],
            "chunks_used": 0,
        }

    context = build_context(chunks)
    answer = generate_answer(query, context)

    sources = list({chunk["metadata"].get("document_id") for chunk in chunks if chunk["metadata"].get("document_id")})

    return {
        "answer": answer,
        "sources": sources,
        "chunks_used": len(chunks),
        "relevance_scores": {chunk["metadata"].get("document_id", f"chunk_{i}"): chunk["score"] for i, chunk in enumerate(chunks)},
    }


def generate_chat_title(question: str, answer: str) -> str:
    prompt = (
        "Generate a very short, concise, and descriptive title for a chat session based on the following question and answer.\n\n"
        f"Question: {question}\n"
        f"Answer: {answer}\n\n"
        "Title:"
    )
    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content.strip().strip('"')


def generate_chat_description(question: str, answer: str) -> str:
    prompt = (
        "Generate a concise and informative description for a chat session based on the following question and answer. Make it short and to the point.\n\n"
        f"Question: {question}\n"
        f"Answer: {answer}\n\n"
        "Description:"
    )
    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content.strip().strip('"')



def calc_relevance_score(similarity_score: float) -> float:
    # Convert cosine similarity (-1 to 1) to a relevance score (0 to 100)
    return max(0, min(100, (similarity_score + 1) / 2 * 100))
```

---

## 29. `app/ai/rag/vector_store.py`

```python
from langchain_chroma import Chroma
from .embedder import get_embedding_model
from ...core.config import CHROMA_PERSISTENCE_DIR


vector_store = Chroma(
    persist_directory=CHROMA_PERSISTENCE_DIR,
    embedding_function=get_embedding_model(),
    # collection_name="knowledge_base_vector_store",
    collection_name="knowledge_base_db_vectors",
)
```

---

## 30. `app/api/__init__.py`

```python
from .router import api_router

__all__ = ["api_router"]
```

---

## 31. `app/api/router.py`

```python
from fastapi import APIRouter
from .endpoints import auth_router, document_router, chat_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(document_router)
api_router.include_router(chat_router)
```

---

## 32. `app/api/endpoints/__init__.py`

```python
from .auth import auth_router
from .document import document_router
from .chat import chat_router
```

---

## 33. `app/api/endpoints/auth.py`

```python
from fastapi import APIRouter
from ...core.dependencies import DB, CurrentUser
from ...schemas import UserCreate, UserLogin, RefreshTokenRequest, AuthResponse
from ...modules import auth_service

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register", response_model=AuthResponse)
def register(user: UserCreate, db: DB):
    return auth_service.register(user, db)

@auth_router.post("/login", response_model=AuthResponse)
def login(user: UserLogin, db: DB):
    return auth_service.login(user.email, user.password, db)

@auth_router.post("/refresh")
def refresh_access_token(token: RefreshTokenRequest,  db: DB):
    return auth_service.refresh_access_token(token.refresh_token, db)

@auth_router.post("/revoke")
def revoke_refresh_token(token: RefreshTokenRequest, db: DB):
    return auth_service.revoke_refresh_token(token.refresh_token, db)
@auth_router.post("/logout")
def logout(current_user: CurrentUser, db: DB):
    return auth_service.logout(current_user.id, db)
```

---

## 34. `app/api/endpoints/chat.py`

```python
from fastapi import APIRouter
from ...modules.chat_service import send_message, get_chat_history, list_user_chat_sessions, list_all_chat_sessions
from ...core.dependencies import DB
from ...schemas.chat import ChatRequest


chat_router = APIRouter(prefix="/chat", tags=["chat"])

@chat_router.post("/")
def chat(db: DB, request: ChatRequest):
    return send_message(db, session_id=request.session_id, question=request.question)

@chat_router.get("/{session_id}/history")
def get_history(session_id: str, db: DB, limit: int = 100):
    return get_chat_history(db, session_id=session_id, limit=limit)


@chat_router.get("/sessions")
def list_all_sessions(db: DB, limit: int = 100):
    return list_all_chat_sessions(db, limit=limit)

@chat_router.get("/sessions/user/{user_id}")
def list_user_sessions(user_id: str, db: DB, limit: int = 100):
    return list_user_chat_sessions(db, user_id=user_id, limit=limit)
```

---

## 35. `app/api/endpoints/document.py`

```python
from fastapi import APIRouter, UploadFile, File, Form, Request, Depends
from fastapi.responses import FileResponse
from ...modules import document_service
from ...core.dependencies import DB, get_current_user
from ...core.exceptions import NotFoundException
from ...schemas.document import DocumentCreate, DocumentResponse
from ...db.models import Document
from uuid import UUID
from pathlib import Path
from ...core.config import UPLOADED_FILES_DIR

document_router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    # dependencies=[Depends(get_current_user)]
)


@document_router.post("/", response_model=DocumentResponse)
def upload_document(
    db: DB,
    # current_user: CurrentUser,
    file: UploadFile = File(..., description="The document file to upload"),
    name: str = Form(...),
    description: str = Form(None),
    author: str = Form(None),
    tags: str = Form(""),
):

    payload = DocumentCreate(
        name=name,
        description=description,
        author=author,
        tags=tags.split(",") if tags else [],
    )
    return document_service.create_document(db, payload, file)


@document_router.get("/")
def list_documents(db: DB, request: Request, limit: int = 100):
    return document_service.get_all_uploaded_documents(db, str(request.base_url), limit)


@document_router.get("/{document_id}")
def get_document(document_id: str, db: DB, request: Request):
    return document_service.get_document_by_id(db, document_id, str(request.base_url))


@document_router.get("/{document_id}/download")
def download_document(document_id: str, db: DB):
    doc = db.query(Document).filter(Document.id == UUID(document_id)).first()
    if not doc:
        raise NotFoundException("Document not found")
    file_path = Path(UPLOADED_FILES_DIR).parent / doc.file_location
    if not file_path.exists():
        raise NotFoundException("File not found on disk")
    return FileResponse(
        path=str(file_path),
        filename=doc.name + doc.file_type,
        # media_type="application/octet-stream",
    )


@document_router.delete("/{document_id}")
def delete_document(document_id: str, db: DB):
    document_service.delete_document(db, document_id)
    return {"message": "Document deleted successfully"}
```

---

## 36. `app/modules/__init__.py`

```python
from .auth_service import (
    register,
    login,
    refresh_access_token,
    revoke_refresh_token,
    logout,
)

__all__ = [
    "register",
    "login",
    "refresh_access_token",
    "revoke_refresh_token",
    "logout",
]
```

---

## 37. `app/modules/auth_service.py`

```python
from ..core.exceptions import (
    BadRequestException,
    ConflictException,
    InternalServerException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
)
from ..core import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token,
    generate_refresh_token,
)
from ..db.models import User, RefreshToken
from ..schemas.user import UserCreate, UserResponse
from datetime import timedelta, datetime, timezone
from sqlalchemy.orm import Session


def register(user: UserCreate, db: Session) -> dict:
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise ConflictException("User with this email already exists", error_detail={"email": user.email})
    hashed_password = hash_password(user.password)
    try:
        new_user = User(name=user.name, email=user.email,
                        password_hash=hashed_password)
    except ValueError as e:
        raise BadRequestException(str(e), error_detail={"email": user.email})
    refresh_token = generate_refresh_token()
    db.add(new_user)
    db.flush()  # Flush to get the new user's ID for the refresh token
    db_refresh_token = RefreshToken(
        user_id=new_user.id,
        token=refresh_token,
        # Refresh token valid for 7 days
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )
    access_token = create_access_token({"sub": str(new_user.id)})
    db.add(db_refresh_token)
    db.commit()
    db.refresh(new_user)
    return {
        "user": UserResponse.model_validate(new_user),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def login(email: str, password: str, db: Session) -> dict:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise UnauthorizedException("Invalid email or password")

    if not verify_password(password, user.password_hash):
        raise UnauthorizedException("Invalid email or password")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = generate_refresh_token()
    db_refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        # Refresh token valid for 7 days
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )
    db.add(db_refresh_token)
    db.commit()
    user_response = UserResponse.model_validate(user)
    return {
        "user": user_response,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def refresh_access_token(refresh_token: str, db: Session) -> dict:
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.is_revoked.is_(False),
        RefreshToken.expires_at > datetime.now(timezone.utc)
    ).first()

    if not db_token:
        raise UnauthorizedException("Invalid or expired refresh token", error_detail={"reason": "Token is invalid, revoked, or expired"})

    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise NotFoundException("User not found", error_detail={"user_id": str(db_token.user_id)})

    db_token.is_revoked = True

    new_refresh_token = generate_refresh_token()
    new_db_token = RefreshToken(
        user_id=user.id,
        token=new_refresh_token,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )
    db.add(new_db_token)
    db.commit()

    access_token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "user": UserResponse.model_validate(user),
    }


def revoke_refresh_token(refresh_token: str, db: Session):
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.is_revoked.is_(False)
    ).first()

    if not db_token:
        raise NotFoundException("Refresh token not found or already revoked", error_detail={"reason": "Token does not exist or has been revoked"})

    db_token.is_revoked = True
    db.commit()

    return {"message": "Refresh token revoked"}


def logout(user_id: str, db: Session):
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.is_revoked.is_(False)
    ).update({"is_revoked": True})
    db.commit()
    return {"message": "Logged out successfully"}
```

---

## 38. `app/modules/chat_service.py`

```python
from sqlalchemy.orm import Session

from ..db.models.enums import MessageRoleEnum
from ..db.models import ChatSession, Message, DocumentChunk, Document
from ..core.exceptions import NotFoundException, BadRequestException
from ..ai.rag.retrieval import (
    retrieve_relevant_chunks,
    build_context,
    llm,
    generate_chat_title,
    generate_chat_description,
)
from ..core.config import INPUT_COST_PER_MILLION, OUTPUT_COST_PER_MILLION, COMPANY_NAME, COMPANY_EMAIL, COMPANY_WEBSITE, AI_NAME
from uuid import UUID
from ..schemas.chat import ChatDocChunkSourceResponse, ChatDocSourceResponse, ChunkSourceResponseInfo


def create_session(db: Session, name: str, user_id: str = None, document_ids: list = None) -> ChatSession:
    generate_title = generate_chat_title(name, "") if not name else name

    title = generate_title if generate_title else "New Chat Session"
    session = ChatSession(
        name=title,
        user_id=user_id,
        document_ids=document_ids or [],
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: str) -> ChatSession:
    try:
        valid_id = UUID(session_id)
    except ValueError:
        raise BadRequestException(
            "Invalid session", error_detail="Invalid session ID format")
    session = db.query(ChatSession).filter(ChatSession.id == valid_id).first()
    if not session:
        raise NotFoundException("Chat session not found")
    return session


def list_user_chat_sessions(db: Session, user_id: str = None, limit: int = 100) -> list[ChatSession]:
    query = db.query(ChatSession).order_by(ChatSession.created_at.desc())
    if user_id:
        try:
            valid_user_id = UUID(user_id)
        except ValueError:
            raise BadRequestException(
                "Invalid user ID format", error_detail={"user_id": user_id})
        query = query.filter(ChatSession.user_id == valid_user_id)
    result = query.limit(limit).all()
    if result is None or len(result) == 0:
        raise NotFoundException("No chat sessions found for the user")
    return result


def list_all_chat_sessions(db: Session, limit: int = 100) -> list[ChatSession]:
    result = db.query(ChatSession).order_by(
        ChatSession.created_at.desc()).limit(limit).all()
    if result is None or len(result) == 0:
        raise NotFoundException("No chat sessions found")
    return result


def get_chat_history(db: Session, session_id: str, limit: int = 100) -> list[Message]:
    session = get_session(db, session_id)
    result = (
        db.query(Message)
        .filter(Message.session_id == session.id)
        .order_by(Message.created_at.asc())
        .limit(limit)
        .all()
    )
    if result is None or len(result) == 0:
        raise NotFoundException("No chat history found for the session")
    return result


def send_message(db: Session, session_id: str | None, question: str) -> dict:

    if not session_id:
        session = create_session(db, name=question)
    else:
        session = get_session(db, session_id)

    user_msg = Message(
        session_id=session.id,
        content=question,
    )
    db.add(user_msg)
    db.flush()

    # Get chat history (last 10 messages for context)
    history = (
        db.query(Message)
        .filter(
            Message.session_id == session.id,
            Message.id != user_msg.id,
        )
        .order_by(Message.created_at.desc())  # newest first
        .limit(20)
        .all()
    )
    history.reverse()  # back to chronological order for the prompt

    # Search ChromaDB for relevant chunks
    search_filter = None
    if session.document_ids:
        search_filter = {"document_id": {
            "$in": [str(d) for d in session.document_ids]}}

    search_query = question
    if history:
        last_messages = [m.content for m in history[-4:]]
        search_query = "Recent conversation:\n" + \
            "\n".join(last_messages) + f"\n\nCurrent question: {question}"

    chunks = retrieve_relevant_chunks(search_query, k=10, filter=search_filter)

    # Enrich from MySQL (get images, tables, extra metadata)
    enriched_chunks = []
    document_ids_used = set()
    relevance_scores = {}

    doc_sources: list[ChatDocChunkSourceResponse] = []

    for chunk in chunks:
        document_id = chunk["metadata"].get("document_id", "unknown")
        document_ids_used.add(document_id)
        relevance_scores[document_id] = max(
            relevance_scores.get(document_id, 0), chunk["score"]
        )

        vector_id = f"{document_id}_chunk_{chunk['metadata'].get('chunk_index', 0)}"
        chunk_data = {
            "id": vector_id,
            "content": chunk["content"],
            "score": chunk["score"],
            "document_id": document_id,
        }

        # Get extra data from MySQL
        db_chunk = (
            db.query(DocumentChunk)
            .filter(DocumentChunk.vector_id == vector_id)
            .first()
        )

        if db_chunk:
            chunk_data["chunk_index"] = db_chunk.chunk_index
            chunk_data["tokens"] = db_chunk.tokens

        enriched_chunks.append(chunk_data)

    for source_chunk in enriched_chunks:
        doc_id = source_chunk.get("document_id")
        if doc_id and doc_id != "unknown":
            doc = db.query(Document).filter(
                Document.id == UUID(doc_id)).first()
            if doc:
                doc_sources.append(
                    ChatDocChunkSourceResponse(
                        document_info=ChatDocSourceResponse(
                            document_id=doc_id,
                            document_name=doc.name,
                            file_path=doc.file_location,
                            description=doc.description,
                            author=doc.author,
                            tag=doc.tags,
                        ),
                        chunk_info=ChunkSourceResponseInfo(
                            chunk_id=source_chunk.get("id"),
                            score=source_chunk.get("score"),
                            content_preview=source_chunk.get("content")[:200],
                        )
                    )
                )

    # for doc_id in document_ids_used:
    #     doc = db.query(Document).filter(Document.id == UUID(doc_id)).first()
    #     if doc:
    #         doc_sources.append({
    #             "document_id": str(doc.id),
    #             "document_name": doc.name,
    #             "description": doc.description,
    #             "author": doc.author,
    #             "tags": doc.tags,
    #         })

    # Build prompt with context + history
    context = build_context(
        chunks) if chunks else "No relevant documents found."

    messages = [
        {
            "role": "system",
            "content": (
                f"You are {AI_NAME}, an AI-powered knowledge base assistant created by Chris Ajuluchukwu Okeke (Emperor Chris) "
                f"for {COMPANY_NAME}.\n\n"
                f"About you:\n"
                f"- Your name is {AI_NAME}\n"
                f"- You were built by Chris Ajuluchukwu Okeke (also known as Emperor Chris), a software engineer\n"
                f"- You serve {COMPANY_NAME} ({COMPANY_WEBSITE})\n"
                f"- For support or inquiries, users can reach out at {COMPANY_EMAIL}\n"
                f"- You are a RAG-based AI assistant that answers questions from uploaded documents\n\n"
                "Behavior rules:\n"
                "1. Answer questions using only the provided context. Do not fabricate information.\n"
                "2. Never include source references like [Source 1], document IDs, chunk IDs, or internal identifiers.\n"
                "3. Write naturally as if you inherently know the information — never say 'the context says' or 'according to the documents'.\n"
                f"4. If asked who you are, introduce yourself as {AI_NAME} and mention your creator.\n"
                "5. If asked something outside the provided context, respond: "
                "'I don't have enough information in my knowledge base to answer that. "
                f"You can contact {COMPANY_EMAIL} for further assistance.'\n"
                "6. Structure longer answers with bullet points or numbered lists for clarity.\n"
                "7. If a question is ambiguous, address the most likely interpretation and note the ambiguity.\n"
                "8. Be concise but thorough — include all relevant details without unnecessary filler.\n"
                "9. Be professional, friendly, and helpful in tone."
            ),
        },
        {"role": "system", "content": f"Context:\n{context}"},
    ]

    # Add chat history (last 10 messages)
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})

    # Add current question
    messages.append({"role": "user", "content": question})

    # Send to LLM
    response = llm.invoke(messages)
    input_tokens = response.usage_metadata.get("input_tokens", 0)
    output_tokens = response.usage_metadata.get("output_tokens", 0)
    estimated_cost = calculate_cost(input_tokens, output_tokens)

    # Save assistant message
    assistant_msg = Message(
        session_id=session.id,
        role=MessageRoleEnum.ASSISTANT.value,
        content=response.content,
        document_ids_used=list(document_ids_used),
        relevance_scores=relevance_scores,
        retrieved_chunk_count=len(enriched_chunks),
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        estimated_cost=estimated_cost,
    )
    db.add(assistant_msg)

    # Update session stats
    session.total_messages += 2
    session.total_tokens += input_tokens + output_tokens
    session.total_cost += estimated_cost

    # Auto-generate title/description on first message
    if session.total_messages == 2:
        session.name = generate_chat_title(question, response.content)
        session.description = generate_chat_description(
            question, response.content)

    db.commit()
    db.refresh(assistant_msg)

    # Return response
    return {
        "message": assistant_msg,
        "sources": doc_sources,
        # "sources": [
        #     {
        #         "document_name":
        #         "document_id": chunk["document_id"],
        #         "content_preview": chunk["content"][:200],
        #         "score": chunk["score"],
        #     }
        #     for chunk in enriched_chunks
        # ],
    }


def delete_session(db: Session, session_id: str) -> dict:
    session = get_session(db, session_id)
    db.delete(session)
    db.commit()
    return {"message": "Session deleted successfully"}


def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    input_cost = (input_tokens / 1_000_000) * INPUT_COST_PER_MILLION
    output_cost = (output_tokens / 1_000_000) * OUTPUT_COST_PER_MILLION
    return round(input_cost + output_cost, 6)
```

---

## 39. `app/modules/document_service.py`

```python

from pathlib import Path

from ..db.models import DocumentSourceEnum

from ..db.models import Document, DocumentChunk
from ..schemas.document import DocumentCreate, DocumentResponse, DocumentChunkResponse
from ..core.exceptions import BadRequestException, NotFoundException
from sqlalchemy.orm import Session
from ..ai.rag.ingestion import ingestion_pipeline
from ..ai.rag.vector_store import vector_store
from fastapi import UploadFile
from ..core.config import UPLOADED_FILES_DIR
import uuid
import tiktoken


encoding = tiktoken.get_encoding("cl100k_base")

def proces_doc_file(file: UploadFile) -> dict:
    filename = file.filename
    filename_without_ext = Path(file.filename).stem

    file_bytes = file.file.read()
    file_size = len(file_bytes)
    file_type = Path(file.filename).suffix
    allowed_types = [".txt", ".pdf", ".md", ".docx", ".html", ".json"]
    if file_type not in allowed_types:
        raise BadRequestException(f"Unsupported file type: {file_type}. Allowed types: {allowed_types}")

    unique_filename = f"{filename_without_ext}_{uuid.uuid4()}{file_type}"
    upload_dir = Path(UPLOADED_FILES_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / unique_filename
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    return {
        "filename": filename,
        "file_bytes": file_bytes,
        "file_size": file_size,
        "file_type": file_type,
        "file_path": str(file_path),
        "file_relative_path": f"{upload_dir.name}/{unique_filename}",
    }


def get_all_uploaded_documents(db: Session, base_url: str, limit: int = 100):
    result = db.query(Document).filter(
        Document.source == DocumentSourceEnum.UPLOADED
    ).order_by(Document.created_at.desc()).limit(limit).all()
    if not result:
        raise NotFoundException("No uploaded documents found")

    documents = []
    for doc in result:
        doc_dict = DocumentResponse.model_validate(doc).model_dump()
        doc_dict["download_url"] = f"{base_url}api/v1/documents/{doc.id}/download"
        documents.append(doc_dict)
    return documents


def get_document_by_id(db: Session, document_id: str, base_url: str):
    try:
        valid_id = uuid.UUID(document_id)
    except ValueError:
        raise BadRequestException("Invalid document ID format")
    doc = db.query(Document).filter(Document.id == valid_id).first()
    if not doc:
        raise NotFoundException("Document not found")
    doc_dict = DocumentResponse.model_validate(doc).model_dump()
    doc_dict["download_url"] = f"{base_url}api/v1/documents/{doc.id}/download"
    return doc_dict


def create_document(db: Session, payload: DocumentCreate, file: UploadFile) -> DocumentResponse:
    doc_file = proces_doc_file(file)
    new_doc = Document(
        name=payload.name,
        description=payload.description,
        file_location=doc_file.get("file_relative_path"),
        file_type=doc_file.get("file_type"),
        size_bytes=doc_file.get("file_size"),
        source=DocumentSourceEnum.UPLOADED,
        author=payload.author,
        tags=payload.tags,
        extra_metadata=payload.extra_metadata,
    )
    db.add(new_doc)
    db.flush()  # Get the new document ID for the ingestion pipeline

    tags_string = ",".join(payload.tags) if payload.tags else ""
    ingest_doc = ingestion_pipeline(doc_file.get("file_bytes"), doc_file.get("filename"), str(new_doc.id), tags_string)

    new_doc.chunks = ingest_doc.get("chunk_count", 0)
    new_doc.is_processed = True
    new_doc.chunk_ids = ingest_doc.get("chunk_ids", [])
    new_doc.total_tables = ingest_doc.get("table_count", 0)
    new_doc.total_images = ingest_doc.get("image_count", 0)
    total_tokens = 0

    for i, (text, vector_id) in enumerate(zip(ingest_doc.get("chunk_texts", []), ingest_doc.get("chunk_ids", []))):
        chunk = DocumentChunk(
            document_id=new_doc.id,
            chunk_index=i,
            content=text,
            tokens=len(encoding.encode(text)),
            vector_id=vector_id,
        )
        total_tokens += chunk.tokens

        db.add(chunk)

    new_doc.tokens = total_tokens
    db.commit()
    db.refresh(new_doc)
    return DocumentResponse.model_validate(new_doc)



def store_document_chunk(db: Session, document_chunk: DocumentChunk) -> DocumentChunkResponse:
    new_chunk = DocumentChunk(
        document_id=document_chunk.document_id,
        chunk_index=document_chunk.chunk_index,
        content=document_chunk.content,
        tokens=document_chunk.tokens,
        vector_id=document_chunk.vector_id,
    )
    db.add(new_chunk)
    db.commit()
    db.refresh(new_chunk)
    return DocumentChunkResponse.model_validate(new_chunk)


def delete_document(db: Session, document_id: str):
    try:
        valid_id = uuid.UUID(document_id)
    except ValueError:
        raise BadRequestException("Invalid document ID format")
    doc = db.query(Document).filter(Document.id == valid_id).first()
    if not doc:
        raise NotFoundException("Document not found")

    # Delete from vector store (ChromaDB)
    vector_store.delete(where={"document_id": str(doc.id)})

    # Delete associated chunks from MySQL
    db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).delete()

    # Delete the document record
    db.delete(doc)
    db.commit()

    # Delete the file from disk
    file_path = Path(UPLOADED_FILES_DIR).parent / doc.file_location
    if file_path.exists():
        file_path.unlink()
```

---

## 40. `app/modules/user_service.py`

```python
```

---

## 41. `app/schemas/__init__.py`

```python
from .chat import ChatCreate, ChatResponse, MessageCreate, MessageResponse
from .document import DocumentCreate, DocumentResponse, DocumentUpdate, DocumentDetailResponse, DocumentChunkResponse
from .user import UserCreate, UserResponse, UserUpdate, UserLogin, RefreshTokenRequest, AuthResponse

__all__ = [
    "ChatCreate",
    "ChatResponse",
    "MessageCreate",
    "MessageResponse",
    "DocumentCreate",
    "DocumentResponse",
    "DocumentUpdate",
    "DocumentDetailResponse",
    "DocumentChunkResponse",
    "UserCreate",
    "UserResponse",
    "UserUpdate",
    "UserLogin",
    "RefreshTokenRequest",
    "AuthResponse",
]
```

---

## 42. `app/schemas/user.py`

```python
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime


# Request: creating a new user
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# Request: updating an existing user
class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


# Response: what the API returns (no password)
class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)



class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
```

---

## 43. `app/schemas/chat.py`

```python
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID
from ..db.models import MessageRoleEnum


class ChatRequest(BaseModel):
    session_id: str | None = None
    question: str = Field(..., min_length=1, description="The question to ask")


class ChatCreate(BaseModel):
    name: str
    description: str | None = None
    user_id: UUID | None = None
    document_ids: list[UUID] | None = None
    total_messages: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    chat_session_id: UUID | None = None


class ChatUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    document_ids: list[UUID] | None = None
    is_active: bool | None = None
    archived_at: datetime | None = None
    total_messages: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0


class ChatResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    document_ids: list[UUID] | None
    chat_session_id: UUID | None
    total_messages: int
    total_tokens: int
    total_cost: float
    is_active: bool
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class MessageCreate(BaseModel):
    role: MessageRoleEnum = MessageRoleEnum.USER
    content: str


class MessageUpdate(BaseModel):
    role: MessageRoleEnum | None = None
    content: str | None = None
    relevance_scores: dict | None = None
    document_ids_used: list[UUID] | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    estimated_cost: float | None = None
    user_rating: int | None = None
    feedback: str | None = None


class MessageResponse(BaseModel):
    id: UUID
    session_id: UUID
    document_id: UUID | None
    role: MessageRoleEnum
    content: str
    document_ids_used: list[UUID] | None
    relevance_scores: dict | None
    retrieved_chunk_count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost: float = 0.0
    user_rating: int = 0
    feedback: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ChatDocSourceResponse(BaseModel):
    document_id: str
    document_name: str
    file_path: str | None
    description: str | None
    author: str | None
    tag: list[str] | None

class ChunkSourceResponseInfo(BaseModel):
    chunk_id: str | None
    score: float
    content_preview: str

class ChatDocChunkSourceResponse(BaseModel):
    document_info: ChatDocSourceResponse
    chunk_info: ChunkSourceResponseInfo
```

---

## 44. `app/schemas/document.py`

```python
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from ..db.models import DocumentSourceEnum


class DocumentCreate(BaseModel):
    name: str
    description: str | None = None
    author: str | None = None
    tags: list[str] | None = None
    extra_metadata: dict | None = None


class DocumentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    author: str | None = None
    tags: list[str] | None = None
    extra_metadata: dict | None = None


class DocumentResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    file_type: str
    size_bytes: int
    source: DocumentSourceEnum
    tags: list[str] | None
    author: str | None
    chunks: int
    tokens: int
    total_tables: int
    total_images: int
    chunk_ids: list[str] | None
    is_processed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentDetailResponse(DocumentResponse):
    content: str
    extra_metadata: dict | None
    chunk_ids: list[str] | None
    relevance_score: float | None


class DocumentChunkResponse(BaseModel):
    id: UUID
    document_id: UUID
    chunk_index: int
    content: str
    tokens: int
    vector_id: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

---

## 45. `app/schemas/refresh_token.py`

```python
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class RefreshTokenResponse(BaseModel):
    id: UUID
    user_id: UUID
    token: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

---

## 46. `alembic/env.py`

```python
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from app.db.database import SQLALCHEMY_DATABASE_URL as DATABASE_URL
from app.db.models.base import Base
from app.db.models import Document, DocumentChunk, ChatSession, User, APILog, RefreshToken  # Import your models here

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

---

## 47. `alembic/versions/587dd353c1e3_add_total_tables_and_images.py`

```python
"""add total_tables and images

Revision ID: 587dd353c1e3
Revises:
Create Date: 2026-04-25 11:47:11.696653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '587dd353c1e3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('documents', sa.Column('total_tables', sa.Integer(), nullable=True))
    op.add_column('documents', sa.Column('total_images', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('documents', 'total_images')
    op.drop_column('documents', 'total_tables')
    # ### end Alembic commands ###
```
