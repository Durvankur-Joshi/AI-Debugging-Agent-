from app.services.embedding_service import embed_text
from app.services.supabase_vector import search_similar_documents


def retrieve_context(error: str, code: str, project_id: str):

    query = f"""
    Error:
    {error}

    Code:
    {code}
    """

    embedding = embed_text(query)

    results = search_similar_documents(
        embedding=embedding,
        project_id=project_id
    )

    if not results:
        return "No relevant context found."

    context = "\n".join([
        result["content"]
        for result in results
    ])

    return context