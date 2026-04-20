from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from ..db.models import MessageRoleEnum

class ChatCreate(BaseModel):
    name: str
    description: str | None = None
    document_ids: list[UUID] | None = None

class ChatResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    document_ids: list[UUID] | None
    total_messages: int
    total_tokens: int
    total_cost: float
    is_active: bool
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
    
    
class MessageCreate(BaseModel):
    role: MessageRoleEnum
    content: str
    document_id: UUID | None = None
    
class MessageResponse(BaseModel):
    id: UUID
    session_id: UUID
    document_id: UUID | None
    role: MessageRoleEnum
    content: str
    document_ids_used: list | None
    relevance_scores: dict | None
    retrieved_chunk_count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost: float = 0.0
    user_rating: int = 0
    feedback: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)