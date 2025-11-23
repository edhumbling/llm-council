"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Council members - list of Groq model identifiers (verified working as of Jan 2025)
# Note: Many Groq models have been decommissioned. Using only currently active models.
COUNCIL_MODELS = [
    "llama-3.3-70b-versatile",      # 280 T/sec, $0.59/$0.79 per 1M tokens
    "llama-3.1-8b-instant",          # 560 T/sec, $0.05/$0.08 per 1M tokens
    "meta-llama/llama-guard-4-12b",  # 1200 T/sec, $0.20/$0.20 per 1M tokens
    "openai/gpt-oss-120b",           # 500 T/sec, $0.15/$0.60 per 1M tokens
    "openai/gpt-oss-20b",            # 1000 T/sec, $0.075/$0.30 per 1M tokens
]

# Chairman model - synthesizes final response
# Using a powerful model for synthesis
CHAIRMAN_MODEL = "llama-3.3-70b-versatile"

# Groq API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Database connection string (Neon PostgreSQL)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_iUGqF31QdZfo@ep-empty-art-a96hqpju-pooler.gwc.azure.neon.tech/neondb?sslmode=require&channel_binding=require"
)
