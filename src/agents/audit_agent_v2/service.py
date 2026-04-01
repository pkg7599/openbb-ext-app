import json
import logging
from typing import AsyncGenerator, Optional

from openbb_ai import QueryRequest, message_chunk
from openbb_ai.models import (
    LlmClientFunctionCallResultMessage,
    LlmClientMessage,
    MessageChunkSSE,
    WidgetCollection,
)

from src.agents.audit_agent_v2.prompt import AUDIT_AGENT_PROMPT, AUDIT_COPILOT_AGENT
from src.custom_google_ai import CustomGoogleAI

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AuditAgentService:

    @staticmethod
    def find_filename(widget: WidgetCollection) -> Optional[str]:
        primary_widgets = widget.primary
        for widget in primary_widgets:
            metadata = widget.metadata
            filename = metadata.get("originalFileName", "")
            if filename:
                return filename
        return None

    @staticmethod
    def retrieve_past_conversation(
        messages: list[LlmClientFunctionCallResultMessage | LlmClientMessage],
        k: int = 10,
    ) -> str:
        past_history = []
        for i, message in enumerate(list(reversed(messages))):
            if i > k:
                return "\n".join(past_history)
            past_history.append(f"{message.role}: {message.content}")
        return "\n".join(past_history)

    @classmethod
    async def execute_query(
        cls,
        query_request: QueryRequest,
    ) -> AsyncGenerator[MessageChunkSSE, None]:
        try:
            route_to_response_planner_agent = False
            logger.info(f"Executing query: {query_request}")
            filename = cls.find_filename(query_request.widgets)
            if filename:
                route_to_response_planner_agent = True

            if route_to_response_planner_agent:
                logger.info("Routing to response planner agent")
                notice_json = open(
                    "resources/extracted_ocr/IndiaTaxAudit2025.json"
                ).read()
                prompt = AUDIT_AGENT_PROMPT.format(audit_notice_text=notice_json)
            else:
                past_conversation = cls.retrieve_past_conversation(
                    query_request.messages
                )

                prompt = AUDIT_COPILOT_AGENT.format(
                    past_history=past_conversation,
                    user_query=query_request.messages[-1].content,
                )
            async for resp_chunk in CustomGoogleAI.chat_completion(content=prompt):
                logger.info(f"Sending chunk: {resp_chunk}")
                if resp_chunk.text:
                    content = resp_chunk.text
                    if content:
                        yield message_chunk(content).model_dump()

        except Exception as err:
            logger.error(f"Error executing query: {err}", exc_info=True)
            raise err
