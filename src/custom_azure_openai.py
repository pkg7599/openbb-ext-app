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
    ENDPOINT = az_openai_settings.endpoint
    API_KEY = az_openai_settings.api_key
    API_VERSION = az_openai_settings.api_version
    EMBED_MODEL = az_openai_settings.embed_model_name
    CHAT_MODEL = az_openai_settings.chat_model_name

    _az_client = None

    @classmethod
    def client(cls):

        if cls._az_client is None:
            cls._az_client = AsyncAzureOpenAI(
                api_key=cls.API_KEY,
                api_version=cls.API_VERSION,
                azure_endpoint=cls.ENDPOINT,
            )
        logger.info("New instance of Azure OpenAI client created")
        return cls._az_client

    @classmethod
    async def embed(cls, inp: EMBED_INPUT_TYPE) -> list[list[float]]:
        try:
            logger.debug(f"Generating embeddings for input: {inp}")
            response = await cls.client().embeddings.create(
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
            return await cls.client().chat.completions.create(
                model=cls.CHAT_MODEL,
                messages=messages,
                stream=stream,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except Exception as e:
            logger.error(f"Error generating chat completions: {e}")
            raise e
