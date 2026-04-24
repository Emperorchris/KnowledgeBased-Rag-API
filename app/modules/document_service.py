from ..db.models import Document, DocumentChunk
from ..schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse, DocumentDetailResponse, DocumentChunkResponse
from ..core.exceptions import NotFoundException, BadRequestException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone
from ..ai.rag.ingestion import ingestion_pipeline
from fastapi import UploadFile


def proces_doc_file(file: UploadFile) -> dict:
    filename = file.filename
    file_bytes = file.file.read()
    file_size = len(file_bytes)
    file_type = filename.split(".")[-1].lower()
    allowed_types = ["txt", "pdf", "md", "docx", "html", "json"]
    if file_type not in allowed_types:
        raise BadRequestException(f"Unsupported file type: {file_type}. Allowed types: {allowed_types}")
    return {
        "filename": filename,
        "file_bytes": file_bytes,
        "file_size": file_size,
        "file_type": file_type,
    }
    
def create_document(db: Session, payload: DocumentCreate, file: UploadFile) -> DocumentResponse:
    doc_file = proces_doc_file(file)
    new_doc = Document(
        name=payload.name,
        description=payload.description,
        file_type=doc_file.get("file_type"),
        size_bytes=doc_file.get("file_size"),
        author=payload.author,
        tags=payload.tags,
        extra_metadata=payload.extra_metadata,
    )
    db.add(new_doc)
    db.flush()  # Get the new document ID for the ingestion pipeline
    
    tags_string = ",".join(payload.tags) if payload.tags else ""
    ingest_doc = ingestion_pipeline(doc_file.get("file_bytes"), doc_file.get("filename"), str(new_doc.id), tags_string)
    
    new_doc.chunks = ingest_doc.get("chunk_count", 0)
    new_doc.is_processed = True
    new_doc.content = ingest_doc.get("enriched_text", "")
    new_doc.chunk_ids = ingest_doc.get("chunk_ids", [])
    
    for i, (text, vector_id) in enumerate(zip(ingest_doc.get("chunk_texts", []), ingest_doc.get("chunk_ids", []))):
        chunk = DocumentChunk(
            document_id=new_doc.id,
            chunk_index=i,
            content=text,
            tokens=len(text.split()),
            vector_id=vector_id,
        )
        db.add(chunk)
    
    db.commit()
    db.refresh(new_doc)
    return DocumentResponse.model_validate(new_doc)



def store_document_chunk(db: Session, document_chunk: DocumentChunk) -> DocumentChunkResponse:
    new_chunk = DocumentChunk(
        document_id=document_chunk.document_id,
        chunk_index=document_chunk.chunk_index,
        content=document_chunk.content,
        tokens=document_chunk.tokens,
        vector_id=document_chunk.vector_id,
    )
    db.add(new_chunk)
    db.commit()
    db.refresh(new_chunk)
    return DocumentChunkResponse.model_validate(new_chunk)
    