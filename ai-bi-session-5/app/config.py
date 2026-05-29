from pathlib import Path
import os
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]

load_dotenv(ROOT_DIR / ".env", override=True)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{ROOT_DIR / 'data' / 'retail_bi.db'}"
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

USE_MOCK_AI = os.getenv("USE_MOCK_AI", "false").strip().lower() == "true"

REPORT_OWNER = os.getenv("REPORT_OWNER", "BI Team")
OUTPUT_DIR = ROOT_DIR / "outputs"