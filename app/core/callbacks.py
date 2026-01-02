import logging
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult


class AgentLoggingCallback(BaseCallbackHandler):
    """
    Log Agent activities: Tool calls, inputs, and outputs.
    """

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        tool_name = serialized.get("name", "tool")
        self.logger.info(f"🛠️ Tool Start: [{tool_name}] Input: {input_str}")

    def on_tool_end(
        self,
        output: Any,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        output_str = str(output)
        truncated_output = (
            output_str[:500] + "..." if len(output_str) > 500 else output_str
        )
        self.logger.info(f"✅ Tool End: Output: {truncated_output}")

    def on_tool_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        self.logger.error(f"❌ Tool Error: {error}")

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        pass
        # self.logger.info("🤖 LLM Thinking...")

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        pass
