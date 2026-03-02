import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response

from src.widgets.chart_widget.service import ChartService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ChartRoute:
    router = APIRouter(prefix="/widgets/chart", tags=["WIDGETS"])

    @staticmethod
    @router.get("/pie/widgets.json", response_model=None)
    async def config() -> Response:
        return JSONResponse(
            content={
                "audit_status_pie_chart": {
                    "name": "Audit Status Pie Chart",
                    "description": "This pie chart depicts audit status",
                    "category": "audit",
                    "type": "chart-highcharts",
                    "endpoint": "",
                    "gridData": {"w": 20, "h": 9},
                }
            }
        )

    @staticmethod
    @router.get("/pie", response_model=None)
    async def get_audit_status_pie_chart_route() -> Response:
        try:
            res = await ChartService.get_audit_status_pie_chart()
        except Exception as e:
            logger.error(f"Error in get_audit_status_pie_chart_route: {str(e)}")
            res = JSONResponse(
                status_code=getattr(e, "status_code", 500),
                content={"message": f"Internal Server Error: {e}"},
            )
        return res
