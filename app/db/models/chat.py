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


