from __future__ import annotations

import asyncio
import logging

from pydantic import BaseModel
from pydantic_ai import Agent

from rp_to_hevy_cli.cache import LLMCache

logger = logging.getLogger(__name__)


async def run_agent_cached[T: BaseModel](
    agent: Agent[None, T],
    user_prompt: str,
    sem: asyncio.Semaphore,
    timeout: float,
    max_retries: int = 3,
    cache: LLMCache | None = None,
    cache_key: str | None = None,
    output_type: type[T] | None = None,
) -> T | None:
    """Run an agent with semaphore, retries, timeout, and optional cache."""
    key = cache_key or user_prompt

    if cache is not None and output_type is not None:
        cached_raw = cache.get(key)
        if cached_raw is not None:
            return output_type.model_validate_json(cached_raw)

    async with sem:
        for attempt in range(max_retries):
            try:
                result = await asyncio.wait_for(agent.run(user_prompt), timeout=timeout)
                output = result.output
                break
            except TimeoutError:
                logger.warning("Timeout (attempt %d/%d)", attempt + 1, max_retries)
                if attempt < max_retries - 1:
                    continue
                return None
            except Exception as exc:
                logger.warning(
                    "Failed (attempt %d/%d): %s", attempt + 1, max_retries, exc
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                return None
        else:
            return None

    if cache is not None:
        cache.set(key, output.model_dump_json())

    return output
