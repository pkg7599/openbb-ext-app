from elasticsearch.dsl import DenseVector, Document, Keyword, Object, Text

from src.db.es_client import ESClient


class VectorDocument(Document):
    content = Text()
    embedding = DenseVector(dims=1536, index=True, similarity="cosine")
    metadata = Object()
    source_id = Keyword()

    class Index:
        name = "vec-doc-index"
        using = ESClient.client()
