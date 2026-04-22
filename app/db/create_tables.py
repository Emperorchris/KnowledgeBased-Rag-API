from .database import engine
from .models.base import Base
from .models import User, Document, DocumentChunk, ChatSession, Message, APILog, DailyStatistics, EmbeddingCache  # noqa: F401
from .models.refresh_token import RefreshToken  # noqa: F401

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()