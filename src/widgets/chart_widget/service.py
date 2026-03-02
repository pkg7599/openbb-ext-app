import logging
from collections import Counter
from typing import Any

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.pie import PieSeries

from config.settings import gcloud_settings
from src.db.bq.bq_client import AsyncBigQueryClient
from src.db.bq.bq_repo import BigQueryRepository
from src.widgets.tabular_widget.model import AuditTrackerBQ

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ChartService:
    _bq_client = AsyncBigQueryClient(
        project_id=gcloud_settings.project_id, credentials=gcloud_settings.credentials
    )

    @classmethod
    async def get_audit_status_pie_chart(cls) -> dict[str, Any]:
        try:
            logger.info("Fetching audit status data from BigQuery")
            audit_tracker_repo = BigQueryRepository(AuditTrackerBQ, cls._bq_client)
            audits: list[AuditTrackerBQ] = await audit_tracker_repo.list(fetch_all=True)
            audit_statuses = [
                audit.status.capitalize()
                for audit in audits
                if audit.status
                in ["CANCELLED", "OPEN", "DRAFT", "COMPLETED", "PENDING"]
            ]
            audit_status_counts = Counter(audit_statuses)
            chart_data = [
                {"name": status, "y": count}
                for status, count in audit_status_counts.items()
            ]
            title = "Audit Status Chart"
            series = PieSeries(name=title, color_by_point=True, data=chart_data)
            options = HighchartsOptions(
                chart={"type": "pie"},
                title={"text": title},
                tooltip={"pointFormat": "<b>{point.percentage:.1f}%</b>"},
                plotOptions={
                    "pie": {
                        "allowPointSelect": True,
                        "cursor": "pointer",
                        "dataLabels": {
                            "enabled": True,
                            "format": "<b>{point.name}</b>: {point.y}",
                        },
                    }
                },
                series=[series],
            )

            chart = Chart.from_options(options)
            return chart.to_dict()
        except Exception as e:
            logger.error(f"Error in get_audit_status_pie_chart: {str(e)}")
            raise e
