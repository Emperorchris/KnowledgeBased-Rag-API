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
