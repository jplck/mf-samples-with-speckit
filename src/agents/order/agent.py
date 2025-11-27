import os
import logging

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import (
    END,
    START,
    MessagesState,
    StateGraph,
)
from typing_extensions import Literal
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from azure.ai.agentserver.langgraph import from_langgraph
from azure.monitor.opentelemetry import configure_azure_monitor

logger = logging.getLogger(__name__)

load_dotenv()

if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    configure_azure_monitor(enable_live_metrics=True, logger_name="__main__")

deployment_name = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")

try:
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential, "https://cognitiveservices.azure.com/.default"
    )
    llm = init_chat_model(
        f"azure_openai:{deployment_name}",
        azure_ad_token_provider=token_provider,
    )
except Exception:
    logger.exception("Order Agent failed to start")
    raise


# Define tools
@tool
def place_order(product_name: str, quantity: int) -> dict:
    """Place an order for a product.

    Args:
        product_name: name of the product to order
        quantity: number of items to order
    """
    import uuid
    import random
    
    # Mock order logic - generate a fake order confirmation
    order_id = str(uuid.uuid4())[:8].upper()
    unit_price = round(random.uniform(10.0, 500.0), 2)
    total_price = round(unit_price * quantity, 2)
    estimated_delivery_days = random.randint(2, 7)
    
    return {
        "order_id": order_id,
        "product_name": product_name,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_price": total_price,
        "status": "confirmed",
        "estimated_delivery_days": estimated_delivery_days
    }


@tool
def check_inventory(product_name: str) -> dict:
    """Check inventory availability for a product.

    Args:
        product_name: name of the product to check
    """
    import random
    
    # Mock inventory check
    in_stock = random.choice([True, True, True, False])  # 75% chance in stock
    available_quantity = random.randint(0, 100) if in_stock else 0
    
    return {
        "product_name": product_name,
        "in_stock": in_stock,
        "available_quantity": available_quantity
    }


# Augment the LLM with tools
tools = [place_order, check_inventory]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

# Nodes
def llm_call(state: MessagesState):
    """LLM decides whether to call a tool or not"""

    return {
        "messages": [
            llm_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful order assistant. You help customers place orders and check product inventory. When a customer wants to order something, use the available tools to check inventory and place orders. Generate friendly, professional order confirmations based on the order results."
                    )
                ]
                + state["messages"]
            )
        ]
    }


def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}


# Conditional edge function to route to the tool node or end based upon whether the LLM made a tool call
def should_continue(state: MessagesState) -> Literal["environment", "__end__"]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]
    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "Action"
    # Otherwise, we stop (reply to the user)
    return END


# Build workflow
def build_agent() -> "StateGraph":
    agent_builder = StateGraph(MessagesState)

    # Add nodes
    agent_builder.add_node("llm_call", llm_call)
    agent_builder.add_node("environment", tool_node)

    # Add edges to connect nodes
    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_conditional_edges(
        "llm_call",
        should_continue,
        {
            "Action": "environment",
            END: END,
        },
    )
    agent_builder.add_edge("environment", "llm_call")

    # Compile the agent
    return agent_builder.compile()

# Build workflow and run agent
if __name__ == "__main__":
    try:
        agent = build_agent()
        adapter = from_langgraph(agent)
        adapter.run()
    except Exception:
        logger.exception("Order Agent encountered an error while running")
        raise