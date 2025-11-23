"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Council members - list of OpenRouter model identifiers (current free models)
COUNCIL_MODELS = [
    "z-ai/glm-4.5-air:free",
    "deepseek/deepseek-r1:free",
    "openai/gpt-oss-20b:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
]

# Chairman model - synthesizes final response (current free model)
# Using deepseek-r1 as chairman since it's reliable and free
CHAIRMAN_MODEL = "deepseek/deepseek-r1:free"

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
