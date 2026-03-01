from typing import Any

from src.custom_azure_openai import CustomAzureOpenAI
from src.db.es_client import ESClient


class SemanticService:
    INDEX_NAME = "vec-doc-index"
    _es_client = ESClient.client()

    @classmethod
    async def search(
        cls,
        query: str,
        quer_vec: list[float] = None,
        k: int = 5,
        source_fields: list[str] = None,
        source_filter: dict[str, Any] = None,
    ):
        if quer_vec is None:
            embeddings = await CustomAzureOpenAI.embed(query)
            if not embeddings:
                raise ValueError("Could not generate embeddings")
            query_vec = embeddings[0]

        _source = {
            "excludes": ["embedding"],
        }
        if source_fields:
            _source = {"includes": source_fields}
        body = {
            "size": k,
            "_source": _source,
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["content^2", "section"],
                            }
                        }
                    ],
                    "filter": [],
                }
            },
            "knn": {
                "field": "embedding",
                "query_vector": query_vec,
                "k": k,
                "num_candidates": 100,
                "filter": [],
            },
        }
        # Optional metadata filter
        if source_filter:
            body["knn"]["filter"].append({"term": source_filter})
            body["query"]["bool"]["filter"].append({"term": source_filter})
        response = await cls._es_client.search(index=cls.INDEX_NAME, body=body)
        return [
            {"score": hit.get("_score"), "document": hit.get("_source")}
            for hit in response["hits"]["hits"]
        ]
