from app.services.embedding_service import embed_text
from app.services.supabase_vector import search_similar 


def retrieve_context(error: str, code: str, project_id: str):
    query = error + "\n" + code

    query_embedding = embed_text(query)

    results = search_similar(query_embedding, project_id)

    context = "\n".join([doc["content"] for doc in results])

    return context