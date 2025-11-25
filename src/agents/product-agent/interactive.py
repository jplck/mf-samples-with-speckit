import asyncio

from agent_framework import AgentRunUpdateEvent
from agent_framework.azure import AzureAIAgentClient
from agent_framework.observability import setup_observability
from dotenv import load_dotenv
from workflow_core import create_agent, get_credential

load_dotenv(override=True)


async def main() -> None:
    """
    The writer and reviewer multi-agent workflow.
    Executing this module initiates the workflow and streams events to the terminal.

    Environment variables required:
    - AZURE_AI_PROJECT_ENDPOINT: Your Microsoft Foundry project endpoint
    - AZURE_AI_MODEL_DEPLOYMENT_NAME: Your Microsoft Foundry model deployment name
    """

    # Initialize observability for visualization.
    # Set enable_sensitive_data to True to include sensitive information such as prompts and responses.
    setup_observability(vs_code_extension_port=4319, enable_sensitive_data=False)

    async with get_credential() as credential:
        async with AzureAIAgentClient(async_credential=credential) as chat_client:
            agent = await create_agent(chat_client, as_agent=False)

            # Run the agent and stream events
            last_executor_id: str | None = None
            async for event in agent.run_stream(
                "Create a slogan for a new electric SUV that is affordable and fun to drive."
            ):
                if isinstance(event, AgentRunUpdateEvent):
                    eid = event.executor_id
                    if eid != last_executor_id:
                        if last_executor_id is not None:
                            print()
                        print(f"{eid}:", end=" ", flush=True)
                        last_executor_id = eid
                    print(event.data, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
