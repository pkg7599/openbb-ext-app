import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_project_root() -> Path:
    """Returns project root folder."""
    project_path = Path(__file__).parent.parent.resolve()
    logger.debug(f"Project root: {project_path}")
    return project_path
