from ..db.models import Document, DocumentChunk
from ..schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse, DocumentDetailResponse, DocumentChunkResponse
from ..core.exceptions import NotFoundException, BadRequestException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone



def extract_doc_context(document: Document) -> str:
    """
    Extracts the full text content of a document by concatenating its chunks in order.
    """
    chunks = sorted(document.chunks, key=lambda c: c.chunk_index)
    return "\n".join(chunk.content for chunk in chunks)