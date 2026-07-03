import os
from pathlib import Path
from dotenv import load_dotenv

# -------------------------------------------------
# Base Path
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# -------------------------------------------------
# Dataset
# -------------------------------------------------

DATA_FILE = BASE_DIR / "data" / "igdtuw_societies_final.xlsx"
print("BASE_DIR:", BASE_DIR)
print("DATA_FILE:", DATA_FILE)

# -------------------------------------------------
# Recommendation Engine Weights
# -------------------------------------------------

SKILL_WEIGHT = 50
DOMAIN_WEIGHT = 20
TIME_WEIGHT = 20
BONUS_WEIGHT = 10

# -------------------------------------------------
# Bedrock / OpenAI Compatible API
# -------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_ID = os.getenv("MODEL_ID")

print("OPENAI_BASE_URL:", OPENAI_BASE_URL)
print("MODEL_ID:", MODEL_ID)