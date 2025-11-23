import asyncio
import os
from dotenv import load_dotenv
from backend.openrouter import query_model
from backend.config import COUNCIL_MODELS, CHAIRMAN_MODEL

load_dotenv()

async def test_connection():
    print(f"Testing Groq API connection...")
    key = os.getenv("GROQ_API_KEY")
    print(f"API Key present: {bool(key)}")
    if key:
        print(f"Key starts with: {key[:10]}...")
    
    print("\nTesting Council Models:")
    for model in COUNCIL_MODELS:
        print(f"Querying {model}...", end=" ", flush=True)
        try:
            response = await query_model(model, [{"role": "user", "content": "Hello"}], timeout=10)
            if response:
                print("✅ Success")
            else:
                print("❌ Failed (None)")
        except Exception as e:
            print(f"❌ Error: {e}")

    print("\nTesting Chairman Model:")
    print(f"Querying {CHAIRMAN_MODEL}...", end=" ", flush=True)
    try:
        response = await query_model(CHAIRMAN_MODEL, [{"role": "user", "content": "Hello"}], timeout=10)
        if response:
            print("✅ Success")
        else:
            print("❌ Failed (None)")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
