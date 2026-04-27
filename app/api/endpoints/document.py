from fastapi import APIRouter, UploadFile, File, Form, Request, Depends
from fastapi.responses import FileResponse
from ...modules.document_service import (
    create_document,
    get_all_uploaded_documents,
    get_document_by_id,
)
from ...core.dependencies import DB, get_current_user
from ...core.exceptions import NotFoundException
from ...schemas.document import DocumentCreate, DocumentResponse
from ...db.models import Document
from uuid import UUID
from pathlib import Path
from ...core.config import UPLOADED_FILES_DIR

document_router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    dependencies=[Depends(get_current_user)]
)


@document_router.post("/", response_model=DocumentResponse)
def upload_document(
    db: DB,
    # current_user: CurrentUser,
    file: UploadFile = File(..., description="The document file to upload"),
    name: str = Form(...),
    description: str = Form(None),
    author: str = Form(None),
    tags: str = Form(""),
):

    payload = DocumentCreate(
        name=name,
        description=description,
        author=author,
        tags=tags.split(",") if tags else [],
    )
    return create_document(db, payload, file)


@document_router.get("/")
def list_documents(db: DB, request: Request, limit: int = 100):
    return get_all_uploaded_documents(db, str(request.base_url), limit)


@document_router.get("/{document_id}")
def get_document(document_id: str, db: DB, request: Request):
    return get_document_by_id(db, document_id, str(request.base_url))


@document_router.get("/{document_id}/download")
def download_document(document_id: str, db: DB):
    doc = db.query(Document).filter(Document.id == UUID(document_id)).first()
    if not doc:
        raise NotFoundException("Document not found")
    file_path = Path(UPLOADED_FILES_DIR).parent / doc.file_location
    if not file_path.exists():
        raise NotFoundException("File not found on disk")
    return FileResponse(
        path=str(file_path),
        filename=doc.name + doc.file_type,
        # media_type="application/octet-stream",
    )


@document_router.delete("/{document_id}")
def delete_document(document_id: str, db: DB):
    delete_document(db, document_id)
    return {"message": "Document deleted successfully"}
