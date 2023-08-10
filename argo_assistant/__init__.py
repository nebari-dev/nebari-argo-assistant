import logging

from dotenv import load_dotenv

load_dotenv(override=True)

logger = logging.getLogger()
logger.setLevel("ERROR")
