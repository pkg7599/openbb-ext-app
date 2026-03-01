from config.settings import gcloud_settings
from src.db.bq.bq_base_model import BigQueryModel


class AuditTrackerBQ(BigQueryModel):

    __table__ = (
        f"{gcloud_settings.project_id}.{gcloud_settings.bq_dataset}.audit_tracker"
    )

    id: str
    title: str
    market: str
    tax_type: str
    owner_id: str
    status: str
