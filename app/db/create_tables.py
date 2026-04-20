from database import engine
from models.base import Base
from models import User, Document, DocumentChunk, ChatSession, Message, APILog, DailyStatistics, EmbeddingCache

Base.metadata.create_all(bind=engine)