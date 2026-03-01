import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response

from src.widgets.tabular_widget.service import TableService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TableRoute:
    router = APIRouter(prefix="/widgets/table", tags=["WIDGETS"])

    @staticmethod
    @router.get("/bq/widgets.json", response_model=None)
    async def config() -> Response:
        return JSONResponse(
            content={
                "bq_audit_tracker_table": {
                    "name": "Audit Tracker BQ Table Widget",
                    "description": "A Audit Tracker BQ table widget",
                    "type": "table",
                    "endpoint": "",
                    "gridData": {"w": 12, "h": 4},
                }
            }
        )

    @staticmethod
    @router.get("/bq", response_model=None)
    async def bq_audit_tracker_table_route() -> Response:
        try:
            res = await TableService.bq_audit_tracker_table()
        except Exception as e:
            logger.error(f"Error in bq_audit_tracker_table service: {e}")
            res = JSONResponse(
                status_code=getattr(e, "status_code", 500), content={"error": str(e)}
            )
        return res
