from .enhance_content import enrich_partitioned_document
from .chunker import  chunk_document_by_recursive_splitter
from .vector_store import vector_store
from .doc_partition import partition_document
from datetime import datetime, timezone


def ingestion_pipeline(file_bytes: bytes, filename: str, document_id: str, tags: str = "") -> dict:
    """
    Main pipeline for ingesting a document into the knowledge base.
    Steps:
    1. Partition document into elements (text, tables, images)
    2. Enrich content (describe images, summarize tables)
    3. Chunk elements by title structure
    4. Append enriched descriptions to chunk texts
    5. Store in vector database (Chroma auto-embeds)
    """
    
    print("Ingesting document...")
    file_type = filename.rsplit(".", 1)[-1].lower()

    partitioned = partition_document(file_bytes, filename)

    enriched = enrich_partitioned_document(partitioned)

    print("Chunking document...")
    
    chunks = chunk_document_by_recursive_splitter(
        enriched["enriched_text"],
        metadata={
            "document_id": document_id,
            "filename": filename,
            "source": "uploaded",
            "upload_date": datetime.now(timezone.utc).isoformat(),
            "file_type": file_type,
            "tags": tags or "",
        },
    )

    # Set chunk_index per chunk
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i


    ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
    vector_store.add_documents(chunks, ids=ids)

    print("Document ingested successfully!")
    return {
        "document_id": document_id,
        "chunk_ids": ids,
        "chunk_texts": [chunk.page_content for chunk in chunks],
        "filename": filename,
        "chunk_count": len(chunks),
        "enriched_text": enriched["enriched_text"],
        "is_enriched": enriched["enriched_text"] != partitioned["text"],
        "text_count": len(partitioned["text"] or []),
        "table_count": len(partitioned["tables"] or []),
        "image_count": len(partitioned["images"] or []),
    }
    
