from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def generate_fix(error: str, code: str, analysis: str):
    prompt = f"""
    You are a senior software engineer.

    Given the error and analysis below, generate a fix.

    Error:
    {error}

    Code:
    {code}

    Analysis:
    {analysis}

    Return output STRICTLY in JSON format:

    {{
      "fix": "...",
      "corrected_code": "...",
      "explanation": "..."
    }}
    """

    response = llm.invoke(prompt)

    return response.content