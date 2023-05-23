import logging


FORMAT = "[%(levelname)s - %(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(format=FORMAT, level=logging.INFO)
