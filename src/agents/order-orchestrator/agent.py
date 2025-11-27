# Copyright (c) Microsoft. All rights reserved.
"""Product Search & Order Orchestrator Agent.

Routes user requests to either a product-search or order-agent capability
and returns a structured JSON response.
"""

from __future__ import annotations

import json
import os
from collections.abc import AsyncIterable
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar

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
You are an intent router for an e-commerce assistant.
Classify the user message into exactly one of three intents.

Respond ONLY with valid JSON (no markdown, no extra text):
{"next_agent":"<agent>","reason":"<short reason>","input":"<user text>"}

<agent> must be one of: product-search | order-agent | none

Rules:
• product-search – browsing, searching, comparing, asking about products,
  OR any request that mentions a product/item the user might want
  (e.g. "I need a table", "looking for headphones") when there is no
  prior conversation context about that specific item.
• order-agent    – placing, modifying, tracking, or cancelling an order,
  BUT only when the user explicitly refers to an existing order or
  a product already identified/selected in the conversation.
• none           – cannot confidently classify.

Important: When in doubt, prefer product-search. A phrase like "I need X"
or "I want X" without prior context about X means the user is looking to
discover or browse products, not place an order yet.
"""

_HUMAN_MESSAGES: dict[str, str] = {
    "product-search": "I'll forward your request to the product search agent to look up relevant items.",
    "order-agent": "I'll send your request to the order agent to help you place or manage an order.",
    "none": "I couldn't clearly determine whether you want to search for products or place an order. Please clarify.",
}

_GREETING: str = (
    "I'm your shopping assistant. Ask me to search for products "
    "or place an order, and I'll route your request to the best capability."
)


# ---------------------------------------------------------------------------
# Structured Output Models
# ---------------------------------------------------------------------------


class NextAgent(str, Enum):
    """Valid downstream agent targets."""

    PRODUCT_SEARCH = "product-search"
    ORDER_AGENT = "order-agent"
    NONE = "none"


class GotoDecision(BaseModel):
    """Routing decision returned by the orchestrator."""

    next_agent: NextAgent = Field(description="The downstream agent to invoke.")
    reason: str = Field(description="Short explanation for the routing decision.")
    user_input: str = Field(description="Original user query forwarded to the next agent.")
    error: str | None = Field(default=None, description="Error details if routing failed.")


class OrchestratorOutput(BaseModel):
    """Structured output returned by the orchestrator agent."""

    human_readable: str = Field(description="A user-friendly summary of what happens next.")
    goto: GotoDecision = Field(description="Machine-readable routing decision.")


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------


class OrderOrchestratorAgent(BaseAgent):
    """Routes incoming messages to downstream product-search or order agents."""

    # Downstream agent identifiers (class-level defaults)
    product_search_agent_name: ClassVar[str] = "product-search"
    order_agent_name: ClassVar[str] = "order-agent"

    def __init__(
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        product_search_agent_name: str | None = None,
        order_agent_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(name=name, description=description, **kwargs)
        if product_search_agent_name:
            self.product_search_agent_name = product_search_agent_name
        if order_agent_name:
            self.order_agent_name = order_agent_name

        # Initialize Azure OpenAI client for intent routing
        self._chat_client = AzureOpenAIChatClient(
            credential=DefaultAzureCredential(),
            api_version="2024-05-01-preview",
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def run(
        self,
        messages: str | ChatMessage | list[str] | list[ChatMessage] | None = None,
        *,
        thread: AgentThread | None = None,
        **kwargs: Any,
    ) -> AgentRunResponse:
        normalized = self._normalize_messages(messages)

        if not normalized:
            goto = GotoDecision(
                next_agent=NextAgent.NONE,
                reason="No user query provided yet.",
                user_input="",
            )
            human_readable = _GREETING
        else:
            user_text = normalized[-1].text or ""
            goto = await self._route(user_text)
            human_readable = _HUMAN_MESSAGES.get(goto.next_agent.value, _HUMAN_MESSAGES["none"])

        output = OrchestratorOutput(human_readable=human_readable, goto=goto)

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

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _route(self, user_text: str) -> GotoDecision:
        """Call the LLM to classify intent and return a GotoDecision."""
        try:
            # Build messages with system prompt and user input
            messages = [
                ChatMessage(role=Role.SYSTEM, text=_SYSTEM_PROMPT),
                ChatMessage(role=Role.USER, text=user_text),
            ]
            response = await self._chat_client.get_response(messages=messages)
            # Extract the text from the response
            if hasattr(response, 'messages') and response.messages:
                raw = response.messages[-1].text or ""
            elif hasattr(response, 'output'):
                raw = response.output
            else:
                raw = str(response)
        except Exception as e:
            return GotoDecision(
                next_agent=NextAgent.NONE,
                reason="LLM routing failed.",
                user_input=user_text,
                error=f"LLM call failed: {type(e).__name__}: {e}",
            )

        if not raw:
            return GotoDecision(
                next_agent=NextAgent.NONE,
                reason="LLM returned empty response.",
                user_input=user_text,
                error="LLM returned empty response",
            )

        try:
            parsed = json.loads(raw.strip())
        except (json.JSONDecodeError, ValueError) as e:
            return GotoDecision(
                next_agent=NextAgent.NONE,
                reason="Failed to parse LLM response.",
                user_input=user_text,
                error=f"JSON parse error: {e}. Raw response: {raw[:500]}",
            )

        raw_agent = parsed.get("next_agent", "none")

        # Map to enum, defaulting to NONE for invalid values
        try:
            next_agent = NextAgent(raw_agent)
        except ValueError:
            next_agent = NextAgent.NONE

        return GotoDecision(
            next_agent=next_agent,
            reason=parsed.get("reason") or "No reason provided.",
            user_input=user_text,
        )


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Load environment variables from .env file for local development
    # Try to load .env from workspace root (3 levels up from this file)
    workspace_root = Path(__file__).resolve().parent.parent.parent.parent
    load_dotenv(dotenv_path=workspace_root / ".env", override=True)
    
    agent = OrderOrchestratorAgent(
        name="order-orchestrator",
        description="Routes user requests to either the product search agent or the order agent.",
    )
    from_agent_framework(agent).run()