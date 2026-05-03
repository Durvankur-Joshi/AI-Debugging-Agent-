from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model = "gemini-embedding-2-preview",
    google_api_key = os.getenv("GOOGLE_API_KEY")
)

def embed_text(text:str):
    return embeddings.embed_query(text)