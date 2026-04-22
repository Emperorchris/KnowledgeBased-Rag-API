from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class RefreshTokenResponse(BaseModel):
    id: UUID
    user_id: UUID
    token: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    