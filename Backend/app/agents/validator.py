from app.services.llm_service import llm
from app.utils.parser import clean_json_response


def validate_fix(error, code, fix):

    prompt = f"""
    You are a senior software engineer.

    Your task is to validate whether the proposed fix correctly solves the error.

    ERROR:
    {error}

    ORIGINAL CODE:
    {code}

    GENERATED FIX:
    {fix}

    Analyze carefully.

    Return ONLY valid JSON:

    {{
      "valid": true,
      "confidence": 95,
      "feedback": "Short explanation about whether the fix is correct."
    }}
    """

    response = llm.invoke(prompt)

    if hasattr(response, "content"):
        text = response.content
    else:
        text = str(response)

    parsed = clean_json_response(text)

    return parsed