import os
from typing import Any, Callable, Dict, List, Optional, Union
from uuid import UUID
from langchain.chat_models import AzureChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult


class CustomCallbackHandler(BaseCallbackHandler):
    """Custom CallbackHandler."""

    streaming_handler: Callable

    def __init__(self, call_back_func: Callable) -> None:
        self.streaming_handler = call_back_func

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        pass

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        pass

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """新しいtokenが来たらコールされる"""
        self.streaming_handler(token)

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Do nothing."""
        pass

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""
        class_name = serialized["name"]
        print(f"\n\n\033[1m> Entering new {class_name} chain...\033[0m")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        print("\n\033[1m> Finished chain.\033[0m")

    def on_chain_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Do nothing."""
        pass

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any,
    ) -> None:
        """Do nothing."""
        pass

    def on_agent_action(
        self, action: AgentAction, color: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """Run on agent action."""
        print(action)

    def on_tool_end(
        self,
        output: str,
        color: Optional[str] = None,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """If not the final action, print out observation."""
        print(output)

    def on_tool_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Do nothing."""
        pass

    def on_text(
        self,
        text: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Run when agent ends."""
        print(text)

    def on_agent_finish(
        self, finish: AgentFinish, color: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Run on agent end."""
        print(finish.log)


class LangchainChatModelFactory:
    @staticmethod
    def create_instance(handle_token: Callable):
        return AzureChatOpenAI(
            callbacks=[CustomCallbackHandler(handle_token)],
            openai_api_base=os.environ.get("AZURE_OPENAI_API_BASE", ""),
            openai_api_version=os.environ.get("AZURE_OPENAI_API_VERSION", ""),
            deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", ""),
            openai_api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
            openai_api_type=os.environ.get("AZURE_OPENAI_API_TYPE", ""),
            streaming=True,
        )
