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


def get_async_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=os.environ["MINIMAX_API_KEY"],
        base_url=os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")
    )


def get_sync_client() -> OpenAI:
    return OpenAI(
        api_key=os.environ["MINIMAX_API_KEY"],
        base_url=os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")
    )


async def call_async(
    system_prompt: str,
    user_message: str,
    temperature: float = 0.3,
    max_tokens: int = 10000
) -> str:
    config = load_config()
    client = get_async_client()
    response = await client.chat.completions.create(
        model=config["model"],
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content


def call_sync(
    system_prompt: str,
    user_message: str,
    temperature: float = 0.3,
    max_tokens: int = 10000
) -> str:
    config = load_config()
    client = get_sync_client()
    response = client.chat.completions.create(
        model=config["model"],
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content


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