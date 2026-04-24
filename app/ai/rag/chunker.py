from unstructured.chunking.title import chunk_by_title
from ...core.config import CHUNK_OVERLAP, CHUNK_SIZE
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_document_by_title(elements, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Chunks a document based on its title structure using the unstructured library's chunk_by_title function.
    This method preserves the logical structure of the document by using titles as natural breakpoints.
    """
    chunks = chunk_by_title(
        elements,
        chunk_size=chunk_size,
        overlap=overlap,
        combine_text_under_n_chars=500, 
        new_after_n_chars=chunk_size + 800 # Fallback to chunking after a certain number of characters if no titles are found within that range
    )
    return chunks


def chunk_document_by_recursive_splitter(text, metadata=None, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.create_documents([text], metadatas=[metadata] if metadata else None)
