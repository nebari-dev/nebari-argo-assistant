from dotenv import load_dotenv
import logging 

load_dotenv(override=True)

logger = logging.getLogger()
logger.setLevel('ERROR')
