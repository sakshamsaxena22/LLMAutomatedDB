from pathlib import Path
import os
from dotenv import load_dotenv

# -------------------------------------------------------------------
# Explicitly load .env from backend/.env (NOT relying on cwd)
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

def get_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(
            f"{key} environment variable is not set. "
            f"Expected in {ENV_PATH}"
        )
    return value
MONGODB_URI: str = get_env("MONGODB_URI")
GROQ_API_KEY: str = get_env("GROQ_API_KEY")

MAX_RESULTS: int = int(os.getenv("MAX_RESULTS", "100"))
