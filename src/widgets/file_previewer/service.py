import base64
import logging
from pathlib import Path

import aiofiles

from config.settings import pdf_docs_settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FilePreviewerService:

    PDF_DOCUMENT_DIRECTORY: Path = pdf_docs_settings.resource_path

    @classmethod
    async def file_preview_service(cls, file_id: str) -> tuple[str, str]:
        """
        This method is responsible for reading the file from the disk and returning the base64 encoded content
        along with the filename.
        :param file_id:
        :return:
        """
        try:
            filename = f"{file_id}.pdf"
            file_path = cls.PDF_DOCUMENT_DIRECTORY / Path(filename)

            if not file_path.exists():
                logger.warning(f"File not found: {file_path}")
                raise FileNotFoundError(f"File not found: {file_path}")

            async with aiofiles.open(file_path, mode="rb") as f:
                content = await f.read()
                encoded_base64_content = base64.b64encode(content).decode("utf-8")
                logger.info(f"File preview service successful for file: {file_path}")
                return filename, encoded_base64_content
        except Exception as e:
            logger.error(f"Error in file preview service: {e}")
            raise e
