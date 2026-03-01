from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.utils import get_project_root


class PDFDocuments(BaseSettings):
    resource_path: Path = Field(
        default=get_project_root() / Path("resources") / Path("documents")
    )

    model_config = SettingsConfigDict(
        env_file=get_project_root() / Path(".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="PDF_",
        env_ignore_empty=True,
    )


class ES(BaseSettings):
    host: str
    api_key: str

    model_config = SettingsConfigDict(
        env_file=get_project_root() / Path(".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="ES_",
        env_ignore_empty=True,
    )


class AzureOpenAI(BaseSettings):
    api_key: str
    endpoint: str
    chat_model_name: str
    embed_model_name: str
    api_version: str

    model_config = SettingsConfigDict(
        env_file=get_project_root() / Path(".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="AZ_",
        env_ignore_empty=True,
    )


pdf_docs_settings = PDFDocuments()
es_settings = ES()
az_openai_settings = AzureOpenAI()
