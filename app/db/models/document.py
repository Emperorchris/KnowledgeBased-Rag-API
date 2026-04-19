from datetime import datetime, timedelta
from sqlalchemy import (
    Column, String, Integer, Text, DateTime, Float, Boolean,
    ForeignKey, Index, Enum, JSON,
)
from sqlalchemy.orm import relationship, validates
import uuid

from .base import Base
from .enums import DocumentSourceEnum


class Document(Base):
    __tablename__ = "documents"

    id = Column(uuid.UUID, primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    file_type = Column(String(10), nullable=False)
    size_bytes = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    source = Column(
        Enum(DocumentSourceEnum, native_enum=False),
        default=DocumentSourceEnum.UPLOADED,
        nullable=False,
    )
    tags = Column(JSON, nullable=True, default=list)
    metadata = Column(JSON, nullable=True, default=dict)
    author = Column(String(255), nullable=True)
    chunks = Column(Integer, default=0)
    tokens = Column(Integer, default=0)
    chunk_ids = Column(JSON, nullable=True, default=list)
    is_processed = Column(Boolean, default=False)
    relevance_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

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
        allowed = ["txt", "pdf", "md", "docx", "html", "json"]
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
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    __table_args__ = (
        Index("ix_document_chunks_document_id", "document_id"),
        Index("ix_document_chunks_vector_id", "vector_id"),
    )

    id = Column(uuid.UUID, primary_key=True, default=uuid.uuid4, unique=True, index=True)
    document_id = Column(
        uuid.UUID,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    tokens = Column(Integer, default=0)
    vector_id = Column(String(255), nullable=True, unique=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    document = relationship("Document", back_populates="chunks_rel")

    def __repr__(self):
        return f"<DocumentChunk doc={self.document_id} index={self.chunk_index}>"
