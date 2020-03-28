import os
import logging

LOGLEVEL = os.environ.get("HARVEST_LOGLEVEL", "INFO")
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger("Harvest API")

__version__ = "0.2.0"
