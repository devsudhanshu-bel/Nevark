import logging
import os

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/nevark.log"

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s",

    handlers=[

        logging.FileHandler(LOG_FILE),

        logging.StreamHandler()
    ]
)

logger = logging.getLogger("NevarkAI")

