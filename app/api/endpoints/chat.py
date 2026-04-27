from fastapi import APIRouter
from ...modules.chat_service import send_message, get_chat_history, list_user_chat_sessions, list_all_chat_sessions
from ...core.dependencies import DB
from ...schemas.chat import ChatRequest


chat_router = APIRouter(prefix="/chat", tags=["chat"])

@chat_router.post("/")
def chat(db: DB, request: ChatRequest):
    return send_message(db, session_id=request.session_id, question=request.question)

@chat_router.get("/{session_id}/history")
def get_history(session_id: str, db: DB, limit: int = 100):
    return get_chat_history(db, session_id=session_id, limit=limit)


@chat_router.get("/sessions")
def list_all_sessions(db: DB, limit: int = 100):
    return list_all_chat_sessions(db, limit=limit)

@chat_router.get("/sessions/user/{user_id}")
def list_user_sessions(user_id: str, db: DB, limit: int = 100):
    return list_user_chat_sessions(db, user_id=user_id, limit=limit)