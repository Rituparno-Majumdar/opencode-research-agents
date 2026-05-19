"""
Minimax API call wrapper.
Supports both async (for parallel agent dispatch) and sync (for Opencode tool calls).
"""

import os
import asyncio
from openai import AsyncOpenAI, OpenAI
import yaml


def load_config() -> dict:
    return yaml.safe_load(open("config.yaml").read())


def get_async_client():
    from google.genai import AsyncClient
    api_key = os.environ.get("GEMINI_API_KEY")
    return AsyncClient(api_key=api_key)


def get_sync_client():
    from google.genai import Client
    api_key = os.environ.get("GEMINI_API_KEY")
    return Client(api_key=api_key)


async def call_async(
    system_prompt: str,
    user_message: str,
    temperature: float = 0.3,
    max_tokens: int = 10000
) -> str:
    config = load_config()
    client = get_async_client()
    
    full_prompt = f"{system_prompt}\n\n{user_message}"
    
    response = await client.models.generate_content(
        model=config["model"],
        contents=[full_prompt],
        config={
            "temperature": temperature,
            "max_output_tokens": max_tokens
        }
    )
    return response.text


def call_sync(
    system_prompt: str,
    user_message: str,
    temperature: float = 0.3,
    max_tokens: int = 10000
) -> str:
    config = load_config()
    client = get_sync_client()
    
    full_prompt = f"{system_prompt}\n\n{user_message}"
    
    response = client.models.generate_content(
        model=config["model"],
        contents=[full_prompt],
        config={
            "temperature": temperature,
            "max_output_tokens": max_tokens
        }
    )
    return response.text


async def call_parallel(calls: list[dict]) -> list[str]:
    """
    Dispatch multiple Minimax calls truly in parallel.
    Each call dict: {system, user, temperature, max_tokens}
    Returns list of responses in same order as input.
    """
    tasks = [
        call_async(
            system_prompt=c["system"],
            user_message=c["user"],
            temperature=c.get("temperature", 0.3),
            max_tokens=c.get("max_tokens", 12000)
        )
        for c in calls
    ]
    return await asyncio.gather(*tasks)