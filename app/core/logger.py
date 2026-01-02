import logging
import sys

# Configure Root Logger for the Application
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger for the given name.
    """
    return logging.getLogger(name)


logger = get_logger("ecos_mcp_server")
