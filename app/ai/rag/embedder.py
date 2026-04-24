from langchain_openai import OpenAIEmbeddings
from ...core.config import OPENAI_API_KEY, EMBEDDING_MODEL


embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL, api_key=OPENAI_API_KEY)

def get_embedding_model() -> OpenAIEmbeddings:
    return embedding_model


def embed_query(text: str) -> list[float]:
    return embedding_model.embed_query(text)


def embed_documents(texts: list[str]) -> list[list[float]]:
    return embedding_model.embed_documents(texts)
