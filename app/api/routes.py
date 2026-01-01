import json
from typing import List

import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.agent.ecos_agent import ecos_agent
from app.repository.statistics import StatisticsRepository, get_statistics_repository
from app.schema.statistics import Statistic
from app.schema.chat import ChatRequest

router = APIRouter()


@router.get("/stats", response_model=List[Statistic])
async def get_stats(
    query: str = "", repo: StatisticsRepository = Depends(get_statistics_repository)
):
    if query:
        return repo.search(query)
    return repo.get_all()


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    inputs = {"messages": [("user", request.message)]}
    result = await ecos_agent.ainvoke(inputs, config=config)

    result["thread_id"] = thread_id
    return result


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    async def event_generator():
        inputs = {"messages": [("user", request.message)]}

        init_payload = {"type": "meta", "thread_id": thread_id}
        yield f"event: meta\ndata: {json.dumps(init_payload)}\n\n"

        async for event in ecos_agent.astream(
            inputs, config=config, stream_mode="updates"
        ):
            for node, content in event.items():
                payload = {}
                if "messages" in content and content["messages"]:
                    msg = content["messages"][-1]
                    payload = {
                        "node": node,
                        "type": msg.type,
                        "content": msg.content,
                        "tool_calls": getattr(msg, "tool_calls", None),
                    }
                else:
                    payload = {"node": node, "content": content}

                json_data = json.dumps(payload, default=str)
                yield f"event: message\ndata: {json_data}\n\n"

        yield "event: completion\ndata: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
