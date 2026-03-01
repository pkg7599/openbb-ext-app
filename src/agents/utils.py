import logging

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionUserMessageParam,
)
from openbb_ai.models import LlmClientFunctionCallResultMessage, LlmClientMessage

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def retrieve_past_conversation(
    messages: list[LlmClientFunctionCallResultMessage | LlmClientMessage], k: int = 5
) -> list[ChatCompletionMessageParam]:
    openai_messages = []
    for ind, message in list(reversed(messages)):
        if ind >= k:
            return list(reversed(openai_messages))
        openai_message = None
        if message.role == "human":
            openai_message = ChatCompletionUserMessageParam(
                content=message.content, role="user"
            )
        elif message.role == "ai":
            openai_message = ChatCompletionAssistantMessageParam(
                content=message.content, role="assistant"
            )
        if openai_message:
            openai_messages.append(openai_message)
    logger.info(f"Retrieved {len(openai_messages)} messages from conversation history")
    return list(reversed(openai_messages))
