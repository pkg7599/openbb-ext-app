import logging
from typing import AsyncGenerator, Optional

from fastapi import HTTPException
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from openbb_ai import QueryRequest, message_chunk
from openbb_ai.models import MessageChunkSSE

from src.agents.audit_agent.prompt import (
    AUDIT_AGENT_SYSTEM_PROMPT,
    AUDIT_AGENT_USER_PROMPT,
)
from src.agents.utils import retrieve_past_conversation
from src.custom_azure_openai import CustomAzureOpenAI
from src.semantic.service import SemanticService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AuditAgentService:

    @staticmethod
    async def execute_query(
        query_request: QueryRequest,
    ) -> AsyncGenerator[MessageChunkSSE, None]:
        logger.info(f"Executing audit query: {query_request}")
        logger.info("Fetching past conversations...")
        user_messages = query_request.messages
        past_messages: list[ChatCompletionMessageParam] = retrieve_past_conversation(
            user_messages
        )
        last_message: Optional[ChatCompletionMessageParam] = (
            past_messages[-1] if past_messages else None
        )

        if last_message is None:
            raise HTTPException(
                status_code=400, detail="No messages found in the request."
            )
        logger.info(f"Last message: {last_message}")

        context = None

        primary_widgets = query_request.widgets.primary
        logger.info(f"Primary widgets: {primary_widgets}")
        for widget in primary_widgets:
            if widget.name == "Document Viewer with fileid":
                file_id = None
                for param in widget.params:
                    if param.name == "file_id":
                        file_id = param.current_value
                        logger.info(f"file_id: {file_id}")
                        break
                if file_id:
                    similar_docs = await SemanticService.search(
                        query=last_message["content"],
                        source_filter={"source_id": file_id},
                    )
                    context = "\n\n".join(
                        doc.get("document", {}).get("content", "")
                        for doc in similar_docs
                    )
        user_prompt = AUDIT_AGENT_USER_PROMPT.format(
            context=context, user_query=last_message["content"]
        )
        openai_messages = (
            [
                ChatCompletionSystemMessageParam(
                    content=AUDIT_AGENT_SYSTEM_PROMPT, role="system"
                )
            ]
            + past_messages[:-1]
            + [ChatCompletionUserMessageParam(content=user_prompt, role="user")]
        )
        stream_response = await CustomAzureOpenAI.chat_completion(
            messages=openai_messages, stream=True
        )
        async for chunk in stream_response:
            logger.info(f"Sending chunk: {chunk}")
            if chunk.choices:
                content = chunk.choices[0].delta.content
                if content:
                    yield message_chunk(content).model_dump()
