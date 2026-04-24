from langchain_openai import ChatOpenAI
from .vector_store import vector_store
from ...core.config import OPENAI_API_KEY, LARGE_LANGUAGE_MODEL


llm = ChatOpenAI(
    model=LARGE_LANGUAGE_MODEL,
    api_key=OPENAI_API_KEY,
    temperature=0,
)


def retrieve_relevant_chunks(query: str, k: int = 5, filter: dict = None) -> list[dict]:
    results = vector_store.similarity_search_with_score(
        query=query,
        k=k,
        filter=filter,
    )
    print(f"Retrieved {len(results)} relevant chunks for query: '{query}'")

    return [
        {
            "content": doc.page_content,
            "metadata": doc.metadata,
            "score": score,
        }
        for doc, score in results
    ]


def build_context(chunks: list[dict]) -> str:
    context_parts = []
    for i, chunk in enumerate(chunks):
        source = chunk["metadata"].get("document_id", "unknown")
        context_parts.append(f"[Source {i + 1} - Document: {source}]\n{chunk['content']}")
    return "\n\n---\n\n".join(context_parts)


def generate_answer(query: str, context: str) -> str:
    prompt = (
        "You are a helpful assistant that answers questions based on the provided context.\n"
        "Only use the information from the context below. If the answer is not in the context, "
        "say \"I don't have enough information to answer that question.\"\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}"
    )

    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content


def query_knowledge_base(query: str, k: int = 5, filter: dict = None) -> dict:
    chunks = retrieve_relevant_chunks(query, k=k, filter=filter)

    if not chunks:
        return {
            "answer": "No relevant documents found for your question.",
            "sources": [],
            "chunks_used": 0,
        }

    context = build_context(chunks)
    answer = generate_answer(query, context)

    sources = list({chunk["metadata"].get("document_id") for chunk in chunks if chunk["metadata"].get("document_id")})

    return {
        "answer": answer,
        "sources": sources,
        "chunks_used": len(chunks),
        "relevance_scores": {chunk["metadata"].get("document_id", f"chunk_{i}"): chunk["score"] for i, chunk in enumerate(chunks)},
    }
