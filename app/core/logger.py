import logging
from rich.logging import RichHandler

def setup_logger(name: str) -> logging.Logger:
    """Creates a stylized logger using Rich."""
    file_handler = logging.FileHandler("friday.log", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s"))
    
    logging.basicConfig(
        level=logging.INFO,
        handlers=[RichHandler(rich_tracebacks=True, markup=True), file_handler]
    )
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

logger = setup_logger("friday")
