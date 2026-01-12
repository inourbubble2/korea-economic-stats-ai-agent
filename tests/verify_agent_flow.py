import asyncio
import os
import sys
import uuid

from dotenv import load_dotenv
from langchain.messages import HumanMessage

sys.path.append(os.getcwd())
load_dotenv()

from app.agent.ecos_agent import ecos_agent  # noqa: E402


async def test_agent_flow():
    query = "코로나 전/후 실업률 차이"
    print(f"\n🙋 User Query: {query}")
    print("-" * 50)

    inputs = {"messages": [HumanMessage(content=query)]}

    current_step = 1
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    async for event in ecos_agent.astream(inputs, config=config, stream_mode="values"):
        messages = event.get("messages")
        if messages:
            last_message = messages[-1]

            sender = last_message.type
            content = last_message.content

            print(f"\n[Step {current_step}] Sender: {sender.upper()}")

            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                for tc in last_message.tool_calls:
                    print(f"🛠️  TOOL CALL: {tc['name']}")
                    print(f"    Args: {tc['args']}")

            if sender == "tool":
                print(f"📦 TOOL OUTPUT (Preview): {str(content)}...")

            if sender == "ai" and not last_message.tool_calls:
                print(f"🤖 AI ANSWER:\n{content}")

            current_step += 1


if __name__ == "__main__":
    asyncio.run(test_agent_flow())
