import json
import re

def extract_json(text: str):
    cleaned = re.sub(r"```json|```", "", text).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", cleaned)
    if match:
        return json.loads(match.group())

    raise ValueError("Invalid AI JSON output")
