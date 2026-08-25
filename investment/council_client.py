"""Thin client for the LLM Council service.

The council (the deliberation lab in the conductor repo, llm-council/) is
called, never duplicated: this module only speaks its HTTP API and returns
the raw deliberation — {stage1, stage2, stage3, metadata}.
"""

import os

import httpx

DEFAULT_BASE_URL = "http://localhost:8001"


def base_url() -> str:
    return os.getenv("COUNCIL_URL", DEFAULT_BASE_URL).rstrip("/")


async def deliberate(brief: str, transport: httpx.AsyncBaseTransport | None = None) -> dict:
    """Run one full council deliberation over the brief and return its result.

    ``transport`` is for tests (httpx.MockTransport); leave None for real use.
    """
    async with httpx.AsyncClient(
        base_url=base_url(), timeout=600.0, transport=transport
    ) as client:
        created = await client.post("/api/conversations", json={})
        created.raise_for_status()
        conversation_id = created.json()["id"]

        answered = await client.post(
            f"/api/conversations/{conversation_id}/message",
            json={"content": brief},
        )
        answered.raise_for_status()
        return answered.json()
