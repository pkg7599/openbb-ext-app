import base64
import json
from pathlib import Path

from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
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
    embed_api_key: str
    embed_endpoint: str
    chat_endpoint: str
    chat_model_name: str
    embed_model_name: str
    embed_api_version: str
    chat_api_version: str
    chat_api_key: str

    model_config = SettingsConfigDict(
        env_file=get_project_root() / Path(".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="AZ_",
        env_ignore_empty=True,
    )


class GoogleCloud(BaseSettings):
    project_id: str
    key_base64: str
    bq_dataset: str

    model_config = SettingsConfigDict(
        env_file=get_project_root() / Path(".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="GCP_",
        env_ignore_empty=True,
    )

    @property
    def gcp_key(self) -> dict:
        return json.loads(base64.b64decode(self.key_base64).decode("utf-8"))

    @property
    def credentials(self) -> Credentials:
        return service_account.Credentials.from_service_account_info(self.gcp_key)


class GoogleAI(BaseSettings):
    api_key: str
    model_name: str

    model_config = SettingsConfigDict(
        env_file=get_project_root() / Path(".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="GOOGLE_AI_",
        env_ignore_empty=True,
    )


pdf_docs_settings = PDFDocuments()
es_settings = ES()
az_openai_settings = AzureOpenAI()
gcloud_settings = GoogleCloud()
google_ai_settings = GoogleAI()
