from app.core.dependencies import get_chat_model
from app.workflow.ecos.state import EcosState
from app.core.logger import get_logger
from langchain_core.messages import SystemMessage, HumanMessage

from datetime import datetime

logger = get_logger(__name__)


async def generate_node(state: EcosState) -> dict:
    llm = get_chat_model()

    fetched_items = state.get("fetched_items", [])
    stat = state["selected_statistic"]
    today = datetime.now().strftime("%Y%m%d")

    items_info = []
    for fetched in fetched_items:
        item = fetched["item"]
        data = fetched["data"]
        items_info.append(f"Item: {item.name} Unit: {data.unit} Values: {data.data}")

    all_items_text = "\n---\n".join(items_info)

    messages = [
        SystemMessage(
            content=f"""You are a Korean Economic Statistics Expert.
You should answer user's query by analyzing the provided statistics.
Current Date: {today} (Today is {today[:4]}-{today[4:6]}-{today[6:]})
- "This year" = {today[:4]}
- "Last year" = {int(today[:4]) - 1}
- Always calculate dates relative to Today.

Key guidelines:
1. DATE AWARENESS:
   - Always analyze data relative to the Current Date.

2. ANALYSIS RULES:
   - Convert large units to Korean readable format (조, 억).
   - If multiple items are provided, compare and analyze them together.
   - PARTIAL DATA HANDLING: If data is available for only PART of the requested period , Present the available data first.
"""
        ),
        HumanMessage(
            content=f"""User Query: {state["query"]}
Statistic: {stat.full_path}
{all_items_text}
Analyze this data and answer the user's question."""
        ),
    ]

    response = await llm.ainvoke(messages)
    return {"messages": [response], "error_message": None}
