import logging
from config.settings import LOGS_PATH

logging.basicConfig(
    filename=LOGS_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
