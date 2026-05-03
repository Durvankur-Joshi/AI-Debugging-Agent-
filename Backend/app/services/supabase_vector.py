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
    
def search_similar_documents(embedding, project_id):

    response = supabase.rpc(
        "match_documents",
        {
            "query_embedding": embedding,
            "match_count": 5,
            "project_id_input": project_id
        }
    ).execute()

    return response.data