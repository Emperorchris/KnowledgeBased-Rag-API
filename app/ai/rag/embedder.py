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
