from typing import Any

from elasticsearch_dsl import Search

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
        is_vectorised: bool = False,
        k: int = 5,
        source_fields: list[str] = None,
        source_filter: dict[str, Any] = None,
    ):
        if quer_vec is None or not is_vectorised:
            embeddings = await CustomAzureOpenAI.embed(query)
            if not embeddings:
                raise ValueError("Could not generate embeddings")
            query_vec = embeddings[0]

        search = Search(using=cls._es_client, index=cls.INDEX_NAME)
        search_query = search.query("multi_match", query=query, type="best_fields")
        if source_filter:
            search_query.filter("term", **source_filter)

        search_query = search_query.knn(
            field="embedding", query_vector=query_vec, k=k, num_candidates=100
        )
        if source_fields:
            search_query = search_query.source(source_fields)
        response = await search_query.execute()
        hits = [
            {{"score": hit.meta.score, "document": hit.to_dict()}}
            for hit in response.hits
        ]
        return hits
