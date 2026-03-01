import logging

from config.settings import gcloud_settings
from src.db.bq.bq_client import AsyncBigQueryClient
from src.db.bq.bq_repo import BigQueryRepository
from src.widgets.tabular_widget.model import AuditTrackerBQ

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TableService:
    _bq_client = AsyncBigQueryClient(
        project_id=gcloud_settings.project_id, credentials=gcloud_settings.credentials
    )

    @classmethod
    async def bq_audit_tracker_table(cls) -> list[AuditTrackerBQ]:
        try:
            audit_tracker_repo = BigQueryRepository(AuditTrackerBQ, cls._bq_client)
            return await audit_tracker_repo.list(fetch_all=True)
        except Exception as e:
            logger.error(f"Error in bq_audit_tracker_table: {str(e)}")
            raise e
