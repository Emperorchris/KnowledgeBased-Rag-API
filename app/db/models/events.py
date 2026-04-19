"""
SQLAlchemy event listeners for automatic timestamp updates.
Import this module once at app startup to register the listeners.
"""

from datetime import datetime
from sqlalchemy import event

from .document import Document
from .chat import ChatSession


@event.listens_for(ChatSession, "before_update")
def update_chat_session_timestamp(mapper, connection, target):
    target.updated_at = datetime.utcnow()


@event.listens_for(Document, "before_update")
def update_document_timestamp(mapper, connection, target):
    target.updated_at = datetime.utcnow()
