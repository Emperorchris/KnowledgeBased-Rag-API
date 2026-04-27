from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID
from ..db.models import MessageRoleEnum


class ChatRequest(BaseModel):
    session_id: str | None = None
    question: str = Field(..., min_length=1, description="The question to ask")


class ChatCreate(BaseModel):
    name: str
    description: str | None = None
    user_id: UUID | None = None
    document_ids: list[UUID] | None = None
    total_messages: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    chat_session_id: UUID | None = None


class ChatUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    document_ids: list[UUID] | None = None
    is_active: bool | None = None
    archived_at: datetime | None = None
    total_messages: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0


class ChatResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    document_ids: list[UUID] | None
    chat_session_id: UUID | None
    total_messages: int
    total_tokens: int
    total_cost: float
    is_active: bool
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class MessageCreate(BaseModel):
    role: MessageRoleEnum = MessageRoleEnum.USER
    content: str


class MessageUpdate(BaseModel):
    role: MessageRoleEnum | None = None
    content: str | None = None
    relevance_scores: dict | None = None
    document_ids_used: list[UUID] | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    estimated_cost: float | None = None
    user_rating: int | None = None
    feedback: str | None = None


class MessageResponse(BaseModel):
    id: UUID
    session_id: UUID
    document_id: UUID | None
    role: MessageRoleEnum
    content: str
    document_ids_used: list[UUID] | None
    relevance_scores: dict | None
    retrieved_chunk_count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost: float = 0.0
    user_rating: int = 0
    feedback: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ChatDocSourceResponse(BaseModel):
    document_id: str
    document_name: str
    file_path: str | None
    description: str | None
    author: str | None
    tag: list[str] | None

class ChunkSourceResponseInfo(BaseModel):
    chunk_id: str | None
    score: float
    content_preview: str

class ChatDocChunkSourceResponse(BaseModel):
    document_info: ChatDocSourceResponse
    chunk_info: ChunkSourceResponseInfo

