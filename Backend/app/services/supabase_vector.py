from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def insert_document(content, embedding, project_id):
    supabase.table("documents").insert({
        "content": content,
        "embedding": embedding,
        "project_id": project_id
    }).execute()
    
def search_similar(query_embedding, project_id):
    return supabase.rpc("match_documents", {
        "query_embedding": query_embedding,
        "match_count": 3,
        "project_filter": project_id
    }).execute().data