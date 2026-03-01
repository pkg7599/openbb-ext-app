import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from src.agents.audit_agent.route import AuditAgentRoute

# from src.middlewares.auth_middleware import AuthMiddleware
from src.widgets.file_previewer.route import FilePreviewerRoute
from src.widgets.tabular_widget.route import TableRoute

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI(
    title="OpenBB External App",
    description="This application contains code for openbb external widgets/apps and copilot agent",
    version="0.0.1",
    docs_url="/docs",
)

app.add_middleware(GZipMiddleware)

# app.add_middleware(AuthMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pro.openbb.co",
        "*",
    ],  # List of origins that can make requests
    allow_credentials=True,  # Allow cookies/authorization headers to be sent
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
@app.get("/health")
async def root():
    return {"message": "OpenBB External App Running!!"}


app.include_router(FilePreviewerRoute.router)
app.include_router(AuditAgentRoute.router)
app.include_router(TableRoute.router)


logger.info(f"OpenBB External App is running!!")
