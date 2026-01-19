import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_quiz_from_text(text: str):
    prompt = f"""
Use ONLY the provided content.

Generate EXACTLY 5 multiple-choice questions.

Difficulty:
- 2 EASY
- 2 MEDIUM
- 1 HARD

STRICT JSON ONLY:

{{
  "quiz_questions": [
    {{
      "difficulty": "easy | medium | hard",
      "question": "",
      "options": ["", "", "", ""],
      "correct_answer": "",
      "explanation": ""
    }}
  ]
}}

CONTENT:
{text}
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text


def generate_related_topics(text: str):
    prompt = f"""
            From the content below, suggest 3–5 related Wikipedia topics.

            Return ONLY JSON array.

            CONTENT:
            {text}
    """

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text
