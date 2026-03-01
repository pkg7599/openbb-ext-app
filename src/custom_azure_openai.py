import logging
from typing import TypeVar

from openai import AsyncAzureOpenAI, AsyncStream
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionMessageParam,
)

from config.settings import az_openai_settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

EMBED_INPUT_TYPE = TypeVar("EMBED_INPUT_TYPE", bound=str | list[str])


class CustomAzureOpenAI:
    EMBED_ENDPOINT = az_openai_settings.embed_endpoint
    EMBED_API_KEY = az_openai_settings.embed_api_key
    EMBED_API_VERSION = az_openai_settings.embed_api_version
    EMBED_MODEL = az_openai_settings.embed_model_name
    CHAT_ENDPOINT = az_openai_settings.chat_endpoint
    CHAT_API_KEY = az_openai_settings.chat_api_key
    CHAT_API_VERSION = az_openai_settings.chat_api_version
    CHAT_MODEL = az_openai_settings.chat_model_name

    _az_embed_client = None
    _az_chat_client = None

    @classmethod
    def embed_client(cls):

        if cls._az_embed_client is None:
            cls._az_embed_client = AsyncAzureOpenAI(
                api_key=cls.EMBED_API_KEY,
                api_version=cls.EMBED_API_VERSION,
                azure_endpoint=cls.EMBED_ENDPOINT,
            )
        logger.info("New instance of Azure OpenAI client created")
        return cls._az_embed_client

    @classmethod
    def chat_client(cls):

        if cls._az_chat_client is None:
            cls._az_chat_client = AsyncAzureOpenAI(
                api_key=cls.CHAT_API_KEY,
                api_version=cls.CHAT_API_VERSION,
                azure_endpoint=cls.CHAT_ENDPOINT,
            )
        logger.info("New instance of Azure OpenAI client created")
        return cls._az_chat_client

    @classmethod
    async def embed(cls, inp: EMBED_INPUT_TYPE) -> list[list[float]]:
        try:
            logger.debug(f"Generating embeddings for input: {inp}")
            response = await cls.embed_client().embeddings.create(
                input=inp,
                model=cls.EMBED_MODEL,
            )
            logger.debug(f"Embeddings generated successfully for input: {inp}")
            embeddings = [data.embedding for data in response.data]
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise e

    @classmethod
    async def chat_completion(
        cls,
        messages: list[dict[str, str] | ChatCompletionMessageParam],
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> ChatCompletion | AsyncStream[ChatCompletionChunk]:
        try:
            logger.debug(f"Generating chat completions for messages: {messages}")
            return await cls.chat_client().chat.completions.create(
                model=cls.CHAT_MODEL,
                messages=messages,
                stream=stream,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except Exception as e:
            logger.error(f"Error generating chat completions: {e}")
            raise e
