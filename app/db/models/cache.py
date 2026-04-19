"""
EmbeddingCache model for avoiding redundant embedding API calls.
"""

from datetime import datetime
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
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_accessed_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<EmbeddingCache hash={self.text_hash[:8]} hits={self.hit_count}>"
