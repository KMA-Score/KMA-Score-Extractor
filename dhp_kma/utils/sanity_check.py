import os
from loguru import logger


def sanity_check():
    if not os.path.join(os.path.abspath("."), "output"):
        logger.info("Output folder not found! Creating...")
        os.mkdir(os.path.join(os.path.abspath("."), "output"))
