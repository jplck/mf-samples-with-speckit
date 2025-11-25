import os
from typing import Any
import asyncio
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.ai.projects.aio import AIProjectClient
import logging

# Import settings to ensure .env is loaded
from config.settings import settings

chat_client = AzureAIAgentClient(
    model_deployment_name="gpt-4.1",
    async_credential=AzureCliCredential(),
    project_endpoint=settings.PROJECT_ENDPOINT,
)

def vacation_tool(from_date: str, to_date: str, reason: str) -> str:
    """Generates a vacation request."""
    return f"Vacation set from {from_date} to {to_date} for reason: {reason}"

def user_profile_tool(user_id: str) -> str:
    """Returns the user profile of the currently logged-in user including (Full name, role, department)"""
    return f"User profile for {user_id}: Name: John Doe, Role: Software Engineer, Department: IT"

# Create agents at module level for devui discovery
hr_agent = chat_client.create_agent(
    name="HR Specialist",
    instructions="Your are an HR specialist agent that handles all employee related questions and tasks. Use your tools to fetch user profiles and other related information as needed.",
    tools=[vacation_tool, user_profile_tool]
).as_tool(
    name="HRSpecialist",
    description="Handles all employee related questions and tasks.",
    arg_name="prompt",
    arg_description="The onboarding or offboarding request details.",
)

technical_support_agent = chat_client.create_agent(
    name="Technical Support Specialist",
    instructions="You are a technical support specialist agent that assists with IT-related issues and requests. This might be hardware or software problems, network issues, general IT support, and hardware procurement requests.",
).as_tool(
    name="TechSupportSpecialist",
    description="Assists with IT-related issues and requests.",
    arg_name="issue",
    arg_description="The IT issue or request details.",
)

agent = chat_client.create_agent(
    name="Orchestrator",
    instructions="Your task is to route prompts and tasks to specialized agents based on user prompts and inquiries. Your agents are connected as tools. Plan your steps carefully and use the available tools to delegate tasks appropriately.",
    tools=[hr_agent, technical_support_agent],
)

async def main():
    async for chunk in agent.run_stream("Onboard a new employee named Alice. Offboard an employee named Bob."):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    asyncio.run(main())
