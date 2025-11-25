import os

from agent_framework import WorkflowBuilder
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import DefaultAzureCredential, ManagedIdentityCredential


def get_credential():
    """Will use Managed Identity when running in Azure, otherwise falls back to DefaultAzureCredential."""
    return (
        ManagedIdentityCredential()
        if os.getenv("MSI_ENDPOINT")
        else DefaultAzureCredential()
    )


async def create_agent(chat_client: AzureAIAgentClient, as_agent: bool = True):
    writer = chat_client.create_agent(
        name="Writer",
        instructions="You are an excellent content writer. You create new content and edit contents based on the feedback.",
    )

    reviewer = chat_client.create_agent(
        name="Reviewer",
        instructions=(
            "You are an excellent content reviewer. "
            "Provide actionable feedback to the writer about the provided content. "
            "Provide the feedback in the most concise manner possible."
        ),
    )

    # Build the workflow by adding agents directly as edges.
    workflow = (
        WorkflowBuilder().set_start_executor(writer).add_edge(writer, reviewer).build()
    )

    return workflow.as_agent() if as_agent else workflow
