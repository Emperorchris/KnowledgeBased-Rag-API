"""
Models package - import everything from here.

Usage:
    from app.db.models import Base, Document, ChatSession, Message
"""

from .base import Base
from .enums import DocumentSourceEnum, MessageRoleEnum
from .document import Document, DocumentChunk
from .chat import ChatSession, Message
from .logging import APILog, DailyStatistics
from .cache import EmbeddingCache

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
]
