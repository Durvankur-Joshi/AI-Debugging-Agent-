import json
import re

def clean_json_response(text: str):
    try:
        # Remove ```json ``` wrapper
        text = re.sub(r"```json|```", "", text).strip()

        # Convert to JSON
        return json.loads(text)

    except Exception as e:
        return {
            "error": "Failed to parse JSON",
            "raw_output": text
        }