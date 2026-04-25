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
_topics_raw = os.getenv("DEFAULT_TOPICS") or ",".join([
    "building AI products in-house",
    "SMS and MMS marketing automation",
    "LLMs vs SLMs in production",
    "deploying Claude on Amazon Bedrock",
    "AI-powered campaign content generation",
    "AI support tools and knowledge bases",
    "lessons from shipping AI features to real clients",
    "the future of marketing automation",
    "prompt engineering for campaign writing",
    "multi-domain content generation systems",
])
DEFAULT_TOPICS = [t.strip() for t in _topics_raw.split(",") if t.strip()]

COMPANY_CONTEXT = """
I work at Textmunication, a marketing automation platform focused on SMS/MMS campaigns.
We're building SAM AI (Smart Automated Messaging) — an in-house AI product suite:

- SAM HELP: A Small Language Model (SLM) support tool that answers service and sales
  questions for our clients and internal team. Its knowledge base is sourced from documents
  stored on AWS S3.

- SAM AI Writer (Campaign Writer): A Large Language Model campaign assistant powered by
  Claude via Amazon Bedrock. It generates content for SMS/MMS marketing campaigns and works
  as a multi-domain content generation system.

My voice on LinkedIn: I'm a builder shipping AI into production at a marketing automation
company — not a commentator. My posts draw from actual work: what's hard about building
SLMs and LLMs for marketing, how SAM HELP and the AI Writer complement each other, what
we've learned deploying Claude on Bedrock, and what's changing in SMS/MMS marketing
because of AI.
""".strip()
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
