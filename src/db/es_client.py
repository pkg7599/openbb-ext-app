from elasticsearch import AsyncElasticsearch

from config.settings import es_settings


class ESClient:
    ES_HOST = es_settings.host
    ES_API_KEY = es_settings.api_key

    _es_client = None

    @classmethod
    def client(cls):
        if cls._es_client is None:
            cls._es_client = AsyncElasticsearch(
                hosts=cls.ES_HOST,
                api_key=cls.ES_API_KEY,
            )
        return cls._es_client
