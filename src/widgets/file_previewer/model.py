from typing import Optional

from pydantic import BaseModel


class DataFormat(BaseModel):
    filename: str
    data_type: str = "pdf"


class FilePreviewResponse(BaseModel):
    headers: dict[str, str | int | float | bool | None] = {
        "Content-Type": "application/json"
    }
    data_format: DataFormat
    content: Optional[str] = None
    file_reference: Optional[str] = None
