from datetime import datetime
from app.core.dependencies import get_chat_model
from app.workflow.ecos.state import EcosState
from app.core.logger import get_logger
from app.schema.statistics import StatisticQueryParametersList, StatisticItem, Statistic
from typing import List
from langchain_core.messages import SystemMessage, HumanMessage

logger = get_logger(__name__)


async def select_parameters_node(state: EcosState) -> dict:
    """Select query parameters (items, dates) using LLM"""
    stat: Statistic = state.get("selected_statistic")
    items: List[StatisticItem] = state.get("found_items", [])

    llm = get_chat_model()
    today = datetime.now().strftime("%Y%m%d")

    options = "\n".join([str(item) for item in items])

    messages = [
        SystemMessage(
            content=f"""You are a korean expert at selecting appropriate economic data parameters.
Current Date: {today} (Today is {today[:4]}-{today[4:6]}-{today[6:]})
- "This year" = {today[:4]}
- "Last year" = {int(today[:4]) - 1}
- Always calculate dates relative to Today.

Key rules:
- If country isn't specified, assume it's Korea.
- Format dates correctly: A(YYYY), Q(YYYYQn), M(YYYYMM), D(YYYYMMDD).
- CHECK Available Range in items! Do not request future dates.
- If user asks for multiple items (e.g., "GDP and unemployment"), select multiple. Otherwise select one.
- If there was a previous error, adjust your parameters (different date format, item, or shorter range)."""
        ),
        HumanMessage(
            content=f"""User Query: {state["query"]}

Selected Statistic: {stat.stat_code} ({stat.stat_name})
Cycle: {stat.cycle.value} (A=Annual, Q=Quarter, M=Month, D=Day)

Available Items:
{options}

PREVIOUS ERROR (if any): {state.get("error_message", "None")}
"""
        ),
    ]

    structured_llm = llm.with_structured_output(StatisticQueryParametersList)
    result: StatisticQueryParametersList = await structured_llm.ainvoke(messages)
    logger.info(f"Selected Params: {result.queries}")

    return {
        "selected_parameters": result.queries,
        "error_message": None,
    }
