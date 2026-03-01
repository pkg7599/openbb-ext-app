import asyncio
from typing import Any

from google.cloud import bigquery
from google.oauth2.service_account import Credentials


class AsyncBigQueryClient:
    def __init__(self, project_id: str, credentials: Credentials):
        self._client = bigquery.Client(project=project_id, credentials=credentials)

    async def query(
        self, query: str, job_config: bigquery.QueryJobConfig | None = None
    ):
        def _run():
            job = self._client.query(query, job_config=job_config)
            return job.result()

        return await asyncio.to_thread(_run)

    async def insert_rows(self, table: str, rows: list[dict[str, Any]]):
        def _run():
            table_ref = self._client.get_table(table)
            return self._client.insert_rows_json(table_ref, rows)

        return await asyncio.to_thread(_run)

    async def delete(self, query: str):
        return await self.query(query)
