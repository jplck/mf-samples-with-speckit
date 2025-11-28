# Copyright (c) Microsoft. All rights reserved.
"""Product Search Agent.

Generates fictional product results based on user search queries.
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterable
from pathlib import Path
from typing import Any

from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from agent_framework import (
    AgentRunResponse,
    AgentRunResponseUpdate,
    AgentThread,
    BaseAgent,
    ChatMessage,
    Role,
    TextContent,
)
from agent_framework.azure import AzureOpenAIChatClient
from azure.ai.agentserver.agentframework import from_agent_framework


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT: str = """\
You are a product generator. Generate product based on a online search with your tool, taking the user's promt as search query.
Output ONLY valid JSON, no markdown, no extra text:
{"name": "<product name>", "price": "<X.XX€>", "description": "<short description>"}
"""


# ---------------------------------------------------------------------------
# Structured Output Models
# ---------------------------------------------------------------------------


class Product(BaseModel):
    """A product search result."""

    name: str = Field(description="The name of the product.")
    price: str = Field(description="The price in EUR format (e.g., '99.99€').")
    description: str = Field(description="A short description of the product.")


class ProductSearchOutput(BaseModel):
    """Structured output returned by the product search agent."""

    human_readable: str = Field(description="A user-friendly summary of the search result.")
    product: Product = Field(description="The generated product.")


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------


class ProductSearchAgent(BaseAgent):
    """Generates product search results based on user queries."""

    def __init__(
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            name=name or "product-search",
            description=description or "Searches for products based on user queries.",
            **kwargs,
        )
        self._chat_client = AzureOpenAIChatClient(
            credential=DefaultAzureCredential(),
            api_version="2024-05-01-preview",
        )

    async def run(
        self,
        messages: str | ChatMessage | list[str] | list[ChatMessage] | None = None,
        *,
        thread: AgentThread | None = None,
        **kwargs: Any,
    ) -> AgentRunResponse:
        normalized = self._normalize_messages(messages)
        user_text = normalized[-1].text if normalized else "something useful"

        # Call LLM to generate product
        llm_messages = [
            ChatMessage(role=Role.SYSTEM, text=_SYSTEM_PROMPT),
            ChatMessage(role=Role.USER, text=user_text),
        ]
        response = await self._chat_client.get_response(messages=llm_messages)

        # Extract response text
        if hasattr(response, 'messages') and response.messages:
            raw = response.messages[-1].text or ""
        elif hasattr(response, 'message'):
            raw = response.message.text or ""
        else:
            raw = str(response)

        # Parse JSON response
        parsed = json.loads(raw.strip())
        product = Product(
            name=parsed.get("name", "Product"),
            price=parsed.get("price", "0.00€"),
            description=parsed.get("description", "A great product."),
        )

        output = ProductSearchOutput(
            human_readable=f"Found: **{product.name}** at {product.price}. {product.description}",
            product=product,
        )

        response_message = ChatMessage(
            role=Role.ASSISTANT,
            contents=[TextContent(text=output.model_dump_json())],
        )

        if thread is not None:
            await self._notify_thread_of_new_messages(thread, normalized, response_message)

        return AgentRunResponse(messages=[response_message])

    async def run_stream(
        self,
        messages: str | ChatMessage | list[str] | list[ChatMessage] | None = None,
        *,
        thread: AgentThread | None = None,
        **kwargs: Any,
    ) -> AsyncIterable[AgentRunResponseUpdate]:
        full = await self.run(messages=messages, thread=thread, **kwargs)
        if full.messages:
            msg = full.messages[0]
            yield AgentRunResponseUpdate(contents=msg.contents, role=msg.role)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    workspace_root = Path(__file__).resolve().parent.parent.parent.parent
    load_dotenv(dotenv_path=workspace_root / ".env", override=True)
    
    agent = ProductSearchAgent(
        name="product-search",
        description="Searches for products based on user queries.",
    )
    from_agent_framework(agent).run()
