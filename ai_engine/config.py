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

# -------------------------------------------------
# Recommendation Engine Weights
# -------------------------------------------------

SKILL_WEIGHT = 45
DOMAIN_WEIGHT = 30
TIME_WEIGHT = 5
BONUS_WEIGHT = 5
ACTIVITY_WEIGHT = 20

# -------------------------------------------------
# Bedrock / OpenAI Compatible API
# -------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_ID = os.getenv("MODEL_ID")