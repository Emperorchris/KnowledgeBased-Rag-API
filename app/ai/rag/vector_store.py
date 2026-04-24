from langchain_chroma import Chroma
from .embedder import get_embedding_model
from ...core.config import CHROMA_PERSISTENCE_DIR


vector_store = Chroma(
    persist_directory=CHROMA_PERSISTENCE_DIR,
    embedding_function=get_embedding_model(),
    # collection_name="knowledge_base_vector_store",
    collection_name="knowledge_base_db_vectors",
)