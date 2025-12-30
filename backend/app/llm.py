import json
from pathlib import Path
from groq import Groq
from app.config import GROQ_API_KEY

PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "mongo_query_prompt.txt"

if not PROMPT_PATH.exists():
    raise RuntimeError(f"Prompt file not found at {PROMPT_PATH}")

SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")

client = Groq(api_key=GROQ_API_KEY)


def generate_query(user_query: str) -> dict:
    if not isinstance(user_query, str) or not user_query.strip():
        raise ValueError("User query must be a non-empty string")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # supported model
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
    )

    raw = response.choices[0].message.content.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError("LLM did not return valid JSON")

    # ✅ HANDLE LLM REFUSAL EXPLICITLY
    if "error" in data:
        raise ValueError(data["error"])

    # ✅ VALID QUERY TYPES
    if "filter" in data:
        data.setdefault("projection", None)
        data.setdefault("sort", [])
        data.setdefault("limit", 100)
        return data

    if "pipeline" in data:
        data.setdefault("limit", 100)
        return data

    raise ValueError("Unknown query type returned by LLM")
