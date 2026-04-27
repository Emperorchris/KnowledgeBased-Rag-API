from sqlalchemy.orm import Session

from ..db.models.enums import MessageRoleEnum
from ..db.models import ChatSession, Message, DocumentChunk, Document
from ..core.exceptions import NotFoundException
from ..ai.rag.retrieval import (
    retrieve_relevant_chunks,
    build_context,
    llm,
    generate_chat_title,
    generate_chat_description,
)
from ..core.config import INPUT_COST_PER_MILLION, OUTPUT_COST_PER_MILLION
from uuid import UUID
from ..schemas.chat import ChatDocChunkSourceResponse, ChatDocSourceResponse, ChunkSourceResponseInfo


def create_session(db: Session, name: str, user_id: str = None, document_ids: list = None) -> ChatSession:
    generate_title = generate_chat_title(name, "") if not name else name

    title = generate_title if generate_title else "New Chat Session"
    session = ChatSession(
        name=title,
        user_id=user_id,
        document_ids=document_ids or [],
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: str) -> ChatSession:
    session = db.query(ChatSession).filter(
        ChatSession.id == UUID(session_id)).first()
    if not session:
        raise NotFoundException("Chat session not found")
    return session


def list_user_chat_sessions(db: Session, user_id: str = None, limit: int = 100) -> list[ChatSession]:
    query = db.query(ChatSession).order_by(ChatSession.created_at.desc())
    if user_id:
        query = query.filter(ChatSession.user_id == user_id)
    return query.limit(limit).all()


def list_all_chat_sessions(db: Session, limit: int = 100) -> list[ChatSession]:
    return db.query(ChatSession).order_by(ChatSession.created_at.desc()).limit(limit).all()


def get_chat_history(db: Session, session_id: str, limit: int = 100) -> list[Message]:
    session = get_session(db, session_id)
    return (
        db.query(Message)
        .filter(Message.session_id == session.id)
        .order_by(Message.created_at.asc())
        .limit(limit)
        .all()
    )


def send_message(db: Session, session_id: str | None, question: str) -> dict:

    if not session_id:
        session = create_session(db, name=question)
    else:
        session = get_session(db, session_id)

    user_msg = Message(
        session_id=session.id,
        content=question,
    )
    db.add(user_msg)
    db.flush()

    # Get chat history (last 10 messages for context)
    history = (
        db.query(Message)
        .filter(
            Message.session_id == session.id,
            Message.id != user_msg.id,
        )
        .order_by(Message.created_at.desc())  # newest first
        .limit(20)
        .all()
    )
    history.reverse()  # back to chronological order for the prompt

    # Search ChromaDB for relevant chunks
    search_filter = None
    if session.document_ids:
        search_filter = {"document_id": {
            "$in": [str(d) for d in session.document_ids]}}


    search_query = question
    if history:
        last_messages = [m.content for m in history[-4:]]
        search_query = "Recent conversation:\n" + \
            "\n".join(last_messages) + f"\n\nCurrent question: {question}"

    chunks = retrieve_relevant_chunks(search_query, k=10, filter=search_filter)

    # Enrich from MySQL (get images, tables, extra metadata)
    enriched_chunks = []
    document_ids_used = set()
    relevance_scores = {}

    doc_sources: list[ChatDocChunkSourceResponse] = []

    for chunk in chunks:
        document_id = chunk["metadata"].get("document_id", "unknown")
        document_ids_used.add(document_id)
        relevance_scores[document_id] = max(
            relevance_scores.get(document_id, 0), chunk["score"]
        )

        vector_id = f"{document_id}_chunk_{chunk['metadata'].get('chunk_index', 0)}"
        chunk_data = {
            "id": vector_id,
            "content": chunk["content"],
            "score": chunk["score"],
            "document_id": document_id,
        }

        # Get extra data from MySQL
        db_chunk = (
            db.query(DocumentChunk)
            .filter(DocumentChunk.vector_id == vector_id)
            .first()
        )

        if db_chunk:
            chunk_data["chunk_index"] = db_chunk.chunk_index
            chunk_data["tokens"] = db_chunk.tokens

        enriched_chunks.append(chunk_data)

    for source_chunk in enriched_chunks:
        doc_id = source_chunk.get("document_id")
        if doc_id and doc_id != "unknown":
            doc = db.query(Document).filter(
                Document.id == UUID(doc_id)).first()
            if doc:
                doc_sources.append(
                    ChatDocChunkSourceResponse(
                        document_info=ChatDocSourceResponse(
                            document_id=doc_id,
                            document_name=doc.name,
                            file_path=doc.file_location,
                            description=doc.description,
                            author=doc.author,
                            tag=doc.tags,
                        ),
                        chunk_info=ChunkSourceResponseInfo(
                            chunk_id=source_chunk.get("id"),
                            score=source_chunk.get("score"),
                            content_preview=source_chunk.get("content")[:200],
                        )
                    )
                )

    # for doc_id in document_ids_used:
    #     doc = db.query(Document).filter(Document.id == UUID(doc_id)).first()
    #     if doc:
    #         doc_sources.append({
    #             "document_id": str(doc.id),
    #             "document_name": doc.name,
    #             "description": doc.description,
    #             "author": doc.author,
    #             "tags": doc.tags,
    #         })

    # Build prompt with context + history
    context = build_context(
        chunks) if chunks else "No relevant documents found."

    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert knowledge base assistant. Your role is to provide accurate, "
                "well-structured answers based strictly on the provided context.\n\n"
                "Rules:\n"
                "1. Only use information from the provided context to answer questions.\n"
                "2. Do NOT include source references like [Source 1], [Source N], or any citation markers in your answer.\n"
                "3. Do NOT include or mention document IDs, chunk IDs, or any internal identifiers.\n"
                "4. If the context does not contain enough information to answer, clearly state: "
                "'Based on the available documents, I don't have enough information to answer this question.'\n"
                "5. Do not make up or infer information beyond what the context provides.\n"
                "6. Structure longer answers with bullet points or numbered lists for clarity.\n"
                "7. If the question is ambiguous, address the most likely interpretation and note the ambiguity.\n"
                "8. Keep answers concise but thorough — include all relevant details from the context.\n"
                "9. Write naturally as if you already know the information — do not reference 'the context' or 'the documents'."
            ),

        },
        {"role": "system", "content": f"Context:\n{context}"},
    ]

    # Add chat history (last 10 messages)
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})

    # Add current question
    messages.append({"role": "user", "content": question})

    # Send to LLM
    response = llm.invoke(messages)
    input_tokens = response.usage_metadata.get("input_tokens", 0)
    output_tokens = response.usage_metadata.get("output_tokens", 0)
    estimated_cost = calculate_cost(input_tokens, output_tokens)

    # Save assistant message
    assistant_msg = Message(
        session_id=session.id,
        role=MessageRoleEnum.ASSISTANT.value,
        content=response.content,
        document_ids_used=list(document_ids_used),
        relevance_scores=relevance_scores,
        retrieved_chunk_count=len(enriched_chunks),
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        estimated_cost=estimated_cost,
    )
    db.add(assistant_msg)

    # Update session stats
    session.total_messages += 2
    session.total_tokens += input_tokens + output_tokens
    session.total_cost += estimated_cost

    # Auto-generate title/description on first message
    if session.total_messages == 2:
        session.name = generate_chat_title(question, response.content)
        session.description = generate_chat_description(
            question, response.content)

    db.commit()
    db.refresh(assistant_msg)

    # Return response
    return {
        "message": assistant_msg,
        "sources": doc_sources,
        # "sources": [
        #     {
        #         "document_name":
        #         "document_id": chunk["document_id"],
        #         "content_preview": chunk["content"][:200],
        #         "score": chunk["score"],
        #     }
        #     for chunk in enriched_chunks
        # ],
    }


def delete_session(db: Session, session_id: str) -> dict:
    session = get_session(db, session_id)
    db.delete(session)
    db.commit()
    return {"message": "Session deleted successfully"}


def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    input_cost = (input_tokens / 1_000_000) * INPUT_COST_PER_MILLION
    output_cost = (output_tokens / 1_000_000) * OUTPUT_COST_PER_MILLION
    return round(input_cost + output_cost, 6)
