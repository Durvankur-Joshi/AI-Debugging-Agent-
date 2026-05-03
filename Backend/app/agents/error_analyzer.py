from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def analyze_error(error: str, code: str , context : str):
    prompt = f"""
        You are a debugging expert.

        Use the provided context if relevant.

        Context:
        {context}

        Error:
        {error}

        Code:
        {code}

        Return JSON:
        {{
          "root_cause": "...",
          "explanation": "..."
        }}
        """

    response = llm.invoke(prompt)

    # ✅ Return only text
    return response.content