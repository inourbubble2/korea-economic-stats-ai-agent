from app.core.dependencies import get_chat_model
from app.workflow.ecos.state import EcosState
from app.schema.statistics import SelectedStatistic
from app.core.logger import get_logger
from langchain_core.messages import SystemMessage, HumanMessage

logger = get_logger(__name__)


async def select_statistic_node(state: EcosState) -> dict:
    """Select the best statistic from found_statistics using LLM"""
    stats = state.get("found_statistics", [])

    llm = get_chat_model()

    options = "\n".join(
        [
            f"- {stat.stat_code}: {stat.full_path} (Cycle: {stat.cycle.value})"
            for stat in stats
        ]
    )
    logger.debug(f"Available Statistics:\n{options}")

    messages = [
        SystemMessage(
            content="""You are a korean expert at selecting the most relevant economic statistic based on user queries."""
        ),
        HumanMessage(
            content=f"""User Query: {state["query"]}

Available Statistics:
{options}

Select the SINGLE best statistic that matches the user's intent."""
        ),
    ]

    structured_llm = llm.with_structured_output(SelectedStatistic)
    selection: SelectedStatistic = await structured_llm.ainvoke(messages)

    selected_stat = next(
        (stat for stat in stats if stat.stat_code == selection.stat_code), None
    )

    return {
        "selected_statistic": selected_stat,
        "error_message": None
        if selected_stat
        else "Selected statistic code not found in options.",
    }
