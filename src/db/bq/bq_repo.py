from typing import Generic, Optional, Type, TypeVar

from google.cloud import bigquery

from src.db.bq.bq_base_model import BigQueryModel
from src.db.bq.bq_client import AsyncBigQueryClient

T = TypeVar("T", bound=BigQueryModel)


class BigQueryRepository(Generic[T]):

    def __init__(self, model: Type[T], client: AsyncBigQueryClient):
        self.model = model
        self.client = client
        self.table = model.__table__

    async def create(self, obj: T) -> None:
        rows = [obj.to_bq_dict()]
        errors = await self.client.insert_rows(self.table, rows)
        if errors:
            raise Exception(errors)

    async def bulk_create(self, objs: list[T]) -> None:
        rows = [o.to_bq_dict() for o in objs]
        errors = await self.client.insert_rows(self.table, rows)
        if errors:
            raise Exception(errors)

    async def get_by_id(self, id_field: str, value: str) -> Optional[T]:
        query = f"""
        SELECT *
        FROM `{self.table}`
        WHERE {id_field} = @value
        LIMIT 1
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("value", "STRING", value)]
        )

        rows = await self.client.query(query, job_config)
        result = list(rows)
        if not result:
            return None

        return self.model(**dict(result[0]))

    async def list(
        self,
        filters: Optional[dict] = None,
        fetch_all: bool = False,
        limit: int = 100,
        offset: int = 0,
    ) -> list[T]:

        where_clause = ""
        query_params = []

        if filters:
            conditions = []
            for i, (key, value) in enumerate(filters.items()):
                param_name = f"param_{i}"
                conditions.append(f"{key} = @{param_name}")
                query_params.append(
                    bigquery.ScalarQueryParameter(param_name, "STRING", value)
                )

            where_clause = "WHERE " + " AND ".join(conditions)

        query = f"""
        SELECT *
        FROM `{self.table}`
        {where_clause}"""

        if not fetch_all:
            query += f"""
        LIMIT {limit}
        OFFSET {offset}
        """

        job_config = bigquery.QueryJobConfig(query_parameters=query_params)

        rows = await self.client.query(query, job_config)
        return [self.model(**dict(row)) for row in rows]

    async def delete_by_id(self, id_field: str, value: str):
        query = f"""
        DELETE FROM `{self.table}`
        WHERE {id_field} = @value
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("value", "STRING", value)]
        )

        await self.client.query(query, job_config)
