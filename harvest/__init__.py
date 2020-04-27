import os
import logging

LOGLEVEL = os.environ.get("HARVEST_LOGLEVEL", "INFO")
logger = logging.getLogger("Harvest API")
logger.setLevel(LOGLEVEL)

__version__ = "0.2.0"
