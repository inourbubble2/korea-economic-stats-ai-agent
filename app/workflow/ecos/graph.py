from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from app.workflow.ecos.state import EcosState
from app.workflow.ecos.nodes import (
    fetch_statistics_node,
    select_statistic_node,
    fetch_items_node,
    select_parameters_node,
    fetch_data_node,
    generate_node,
)


def route_after_fetch_statistics(state: EcosState) -> str:
    if state.get("error_message") or not state.get("found_statistics"):
        retry_count = state.get("retry_count", 0)
        if retry_count < 3:
            state["retry_count"] += 1
            return "fetch_statistics"
        return END

    return "select_statistic"


def route_after_select_statistic(state: EcosState) -> str:
    if state.get("error_message") or not state.get("selected_statistic"):
        retry_count = state.get("retry_count", 0)
        if retry_count < 3:
            state["retry_count"] += 1
            return "select_statistic"
        return END

    return "fetch_items"


def route_after_fetch_items(state: EcosState) -> str:
    if state.get("error_message") or not state.get("found_items"):
        retry_count = state.get("retry_count", 0)
        if retry_count < 3:
            state["retry_count"] += 1
            return "fetch_items"
        return END

    return "select_parameters"


def route_after_select_parameters(state: EcosState) -> str:
    if state.get("error_message") or not state.get("selected_parameters"):
        retry_count = state.get("retry_count", 0)
        if retry_count < 3:
            state["retry_count"] += 1
            return "select_parameters"
        return END

    return "fetch_data"


def route_after_fetch_data(state: EcosState) -> str:
    if state.get("error_message") or not state.get("fetched_items"):
        retry_count = state.get("retry_count", 0)
        if retry_count < 3:
            state["retry_count"] += 1
            return "select_parameters"
        return "generate"

    return "generate"


builder = StateGraph(EcosState)

builder.add_node("fetch_statistics", fetch_statistics_node)
builder.add_node("select_statistic", select_statistic_node)
builder.add_node("fetch_items", fetch_items_node)
builder.add_node("select_parameters", select_parameters_node)
builder.add_node("fetch_data", fetch_data_node)
builder.add_node("generate", generate_node)

builder.add_edge(START, "fetch_statistics")

builder.add_conditional_edges(
    "fetch_statistics",
    route_after_fetch_statistics,
    {
        "select_statistic": "select_statistic",
        "fetch_statistics": "fetch_statistics",
        END: END,
    },
)

builder.add_conditional_edges(
    "select_statistic",
    route_after_select_statistic,
    {
        "fetch_items": "fetch_items",
        "select_statistic": "select_statistic",
        END: END,
    },
)

builder.add_conditional_edges(
    "fetch_items",
    route_after_fetch_items,
    {
        "select_parameters": "select_parameters",
        "fetch_items": "fetch_items",
        END: END,
    },
)

builder.add_conditional_edges(
    "select_parameters",
    route_after_select_parameters,
    {"fetch_data": "fetch_data", "select_parameters": "select_parameters", END: END},
)

builder.add_conditional_edges(
    "fetch_data",
    route_after_fetch_data,
    {
        "select_parameters": "select_parameters",
        "generate": "generate",
        END: END,
    },
)

builder.add_edge("generate", END)

ecos_graph = builder.compile(checkpointer=MemorySaver())
