import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("monitoramento.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)