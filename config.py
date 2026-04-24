import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN", "")
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "")
# GitHub secret is named PRIMARY_CLIENT_SECRET; fallback to LINKEDIN_CLIENT_SECRET for local .env
LINKEDIN_CLIENT_SECRET = os.getenv("PRIMARY_CLIENT_SECRET") or os.getenv("LINKEDIN_CLIENT_SECRET", "")

TIMEZONE = os.getenv("TIMEZONE", "US/Eastern")
_topics_raw = os.getenv("DEFAULT_TOPICS") or "AI,entrepreneurship,productivity,leadership,tech trends"
DEFAULT_TOPICS = [t.strip() for t in _topics_raw.split(",") if t.strip()]
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "ghostwriter.db")

CONTENT_PILLARS = [
    "Thought Leadership",
    "Educational / How-To",
    "Personal Story",
    "Industry Insight",
    "Motivational",
    "Behind the Scenes",
    "Controversial Take",
    "List / Tips",
]

POST_TONES = ["Professional", "Conversational", "Inspirational", "Analytical", "Storytelling"]
