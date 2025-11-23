"""Groq API client for making LLM requests."""

import httpx
from typing import List, Dict, Any, Optional
from .config import GROQ_API_KEY, GROQ_API_URL


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via Groq API.

    Args:
        model: Groq model identifier (e.g., "llama3-8b-8192")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    if not GROQ_API_KEY:
        print("Error: No Groq API key available")
        return None

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                GROQ_API_URL,
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            data = response.json()
            message = data['choices'][0]['message']

            return {
                'content': message.get('content'),
                'reasoning_details': None # Groq doesn't return reasoning details in the same way
            }

    except httpx.HTTPStatusError as e:
        error_detail = ""
        try:
            error_data = e.response.json()
            error_detail = error_data.get('error', {}).get('message', str(e))
        except:
            error_detail = str(e)
        print(f"Error querying model {model}: HTTP {e.response.status_code} - {error_detail}")
        return None
    except Exception as e:
        print(f"Error querying model {model}: {type(e).__name__}: {e}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        models: List of Groq model identifiers
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio

    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model: response for model, response in zip(models, responses)}
