from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

MODEL_NAME = "gemini-2.5-flash"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LIMITS_FILE = str(DATA_DIR / "limits.json")

POLICY_FILE = str(BASE_DIR / "data" / "policy.md")

CHROMA_DB_PATH = str(BASE_DIR / "chroma_db")

APPROVAL_MATRIX_FILE = str(DATA_DIR / "approval_matrix.json")

RECEIPTS_DB_FILE = str(DATA_DIR / "receipts_db.json")