import logging
from typing import AsyncGenerator

from google import genai
from google.genai.types import GenerateContentResponse

from config.settings import google_ai_settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CustomGoogleAI:
    API_KEY = google_ai_settings.api_key
    MODEL_NAME = google_ai_settings.model_name

    _client = None

    @classmethod
    def client(cls) -> genai.Client:
        if not cls._client:
            logger.info("Creating new Google AI client")
            cls._client = genai.Client(api_key=cls.API_KEY)
        logger.info("Returning existing Google AI client")
        return cls._client

    @classmethod
    async def chat_completion(
        cls, content: str
    ) -> AsyncGenerator[GenerateContentResponse, None]:
        try:
            resp_stream = cls.client().models.generate_content_stream(
                model=f"models/{cls.MODEL_NAME}",
                contents=content,
            )
            for chunk in resp_stream:
                logger.info(f"Sending chunk: {chunk}")
                yield chunk
        except Exception as e:
            logger.error(f"Error generating chat completions: {e}")
            raise e
