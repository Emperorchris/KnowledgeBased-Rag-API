from fastapi import APIRouter, UploadFile, File, Form
from ...modules.document_service import create_document
from ...core.dependencies import DB, CurrentUser
from ...schemas.document import DocumentCreate, DocumentResponse

document_router = APIRouter(prefix="/documents", tags=["documents"])


@document_router.post("/", response_model=DocumentResponse)
def upload_document(
    db: DB,
    # current_user: CurrentUser,
    # files: list[UploadFile] = File(..., description="The document file(s) to upload"),
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
    # results = []
    # for file in files:
    #     result = create_document(db, payload, file)
    #     results.append(result)
    # return results
    
    return create_document(db, payload, file)
