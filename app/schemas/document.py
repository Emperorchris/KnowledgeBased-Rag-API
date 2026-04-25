from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from ..db.models import DocumentSourceEnum


class DocumentCreate(BaseModel):
    name: str
    description: str | None = None
    author: str | None = None
    tags: list[str] | None = None
    extra_metadata: dict | None = None


class DocumentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    author: str | None = None
    tags: list[str] | None = None
    extra_metadata: dict | None = None


class DocumentResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    file_type: str
    size_bytes: int
    source: DocumentSourceEnum
    tags: list[str] | None
    author: str | None
    chunks: int
    tokens: int
    total_tables: int
    total_images: int
    chunk_ids: list[str] | None
    is_processed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentDetailResponse(DocumentResponse):
    content: str
    extra_metadata: dict | None
    chunk_ids: list[str] | None
    relevance_score: float | None


class DocumentChunkResponse(BaseModel):
    id: UUID
    document_id: UUID
    chunk_index: int
    content: str
    tokens: int
    vector_id: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
