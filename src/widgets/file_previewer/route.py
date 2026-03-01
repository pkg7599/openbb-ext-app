import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response

from src.widgets.file_previewer.model import DataFormat, FilePreviewResponse
from src.widgets.file_previewer.service import FilePreviewerService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FilePreviewerRoute:
    router = APIRouter(prefix="/widgets/file_previewer", tags=["WIDGETS"])

    @staticmethod
    @router.get("", response_model=None)
    async def file_preview_route(file_id: str) -> Response:

        try:
            filename, b64_content = await FilePreviewerService.file_preview_service(
                file_id
            )
            res = FilePreviewResponse(
                data_format=DataFormat(filename=filename), content=b64_content
            )
        except Exception as e:
            logger.error(f"Error in file preview service: {e}")
            res = JSONResponse(
                status_code=getattr(e, "status_code", 500), content={"error": str(e)}
            )
        return res

    @staticmethod
    @router.get("/widgets.json", response_model=None)
    async def config() -> Response:
        return JSONResponse(
            content={
                "file_previewer_using_fileid": {
                    "name": "Document Viewer with fileid",
                    "description": "Display a PDF file with base64 encoding",
                    "endpoint": "",
                    "gridData": {"w": 20, "h": 20},
                    "type": "pdf",
                    "params": [
                        {
                            "paramName": "file_id",
                            "label": "File Id",
                            "description": "Enter file name",
                            "type": "text",
                            "value": "OhioTaxAudit",
                        }
                    ],
                }
            }
        )
