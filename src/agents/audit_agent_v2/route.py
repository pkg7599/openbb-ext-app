import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from openbb_ai import QueryRequest
from sse_starlette import EventSourceResponse

from src.agents.audit_agent_v2.service import AuditAgentService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class AuditAgentRoute:

    router = APIRouter(prefix="/agents/audit/v2")

    @staticmethod
    @router.get("/agents.json", response_model=None)
    async def config() -> Response:
        return JSONResponse(
            content={
                "audit_agent": {
                    "name": "Audit Response Planner Agent",
                    "description": "A agent to fetch audit data from selected widgets and provide response plan around it.",
                    "endpoints": {"query": "query"},
                    "features": {
                        "streaming": True,
                        "widget-dashboard-select": True,
                        "widget-dashboard-search": False,
                    },
                }
            }
        )

    @staticmethod
    @router.post("/query", response_model=None)
    async def query(query_request: QueryRequest) -> Response:
        try:
            res = EventSourceResponse(
                media_type="text/event-stream",
                content=AuditAgentService.execute_query(query_request),
            )
        except Exception as e:
            logger.error(f"Error executing query: {e}", exc_info=True)
            res = JSONResponse(
                content={"error": str(e)}, status_code=getattr(e, "status_code", 500)
            )
        return res
