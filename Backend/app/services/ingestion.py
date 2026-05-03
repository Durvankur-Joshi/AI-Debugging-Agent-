from app.services.repo_loader import load_repo_files
from app.services.chunker import chunk_code
from app.services.embedding_service import embed_text
from app.services.supabase_vector import insert_document

def ingest_repo(repo_path: str , project_id : str):
    files = load_repo_files(repo_path)

    total_chunks = 0

    for file in files:
        chunks = chunk_code(file["content"])

        for chunk in chunks:
            embedding = embed_text(chunk)

            insert_document(chunk, embedding , project_id)

            total_chunks += 1

    return {
        "files_processed": len(files),
        "chunks_created": total_chunks
    }