import json
from pathlib import Path
from groq import Groq

from app.config import GROQ_API_KEY


BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROMPT_PATH = BASE_DIR / "prompts" / "mongo_prompt.txt"

if not PROMPT_PATH.exists():
    raise RuntimeError(f"Prompt file not found at {PROMPT_PATH}")


with PROMPT_PATH.open("r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read().strip()


client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.1-8b-instant"


def generate_query(user_query: str) -> dict:
    if not user_query or not user_query.strip():
        raise ValueError("User query is empty")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
        temperature=0,
        max_tokens=512,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("Groq returned empty response")

    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Groq returned invalid JSON:\n{content}"
        ) from exc
