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
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email format: {e}")
        return value
