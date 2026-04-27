from fastapi import APIRouter
from ...modules.chat_service import send_message
from ...core.dependencies import DB
from ...schemas.chat import ChatRequest


chat_router = APIRouter(prefix="/chat", tags=["chat"])

@chat_router.post("/")
def chat(db: DB, request: ChatRequest):
    return send_message(db, session_id=request.session_id, question=request.question)
