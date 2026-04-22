from unstructured.partition.auto import partition, PartitionStrategy
from unstructured.documents.elements import Table, Image
from io import BytesIO


SUPPORTED_FILE_TYPES = ["txt", "pdf", "md", "docx", "html", "json"]


def partition_document(file_bytes: bytes, filename: str) -> dict:
    file_type = filename.rsplit(".", 1)[-1].lower()

    if file_type not in SUPPORTED_FILE_TYPES:
        raise ValueError(f"Unsupported file type: {file_type}. Supported: {SUPPORTED_FILE_TYPES}")

    elements = partition(
        file=BytesIO(file_bytes),
        metadata_filename=filename,
        infer_table_structure=True,
        strategy=PartitionStrategy.HI_RES,
        extract_image_block_to_payload=True,
        extract_image_block_types=["Image", "Table"],
        skip_infer_table_types=[],
    )


    if not elements:
        raise ValueError("No content could be extracted from the file")

    text_elements = []
    tables = []
    images = []
    
    print(f"--- Proccessed elemnts: {elements} ---")

    for el in elements:
        if isinstance(el, Table):
            tables.append({
                "content": str(el),
                "html": el.metadata.text_as_html if hasattr(el.metadata, "text_as_html") else None,
                "page": el.metadata.page_number,
            })
        elif isinstance(el, Image):
            images.append({
                "content": str(el),
                "image_path": el.metadata.image_path if hasattr(el.metadata, "image_path") else None,
                "page": el.metadata.page_number,
            })
        else:
            text_elements.append(str(el))

    full_text = "\n\n".join(text_elements)

    return {
        "text": full_text,
        "tables": tables,
        "images": images,
        "element_count": len(elements),
        "table_count": len(tables),
        "image_count": len(images),
    }
