import logging 

# log type(prio) debug(10), info(20), warning(30), error(40), critical(50)     
logging.basicConfig(
    filename="game.log",
    filemode="w",  # 'a' appends to existing logs; 'w' overwrites the file every run
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

try:
    pass
    logger.info("Starting game...")
except Exception as e:
    logger.exception(e)