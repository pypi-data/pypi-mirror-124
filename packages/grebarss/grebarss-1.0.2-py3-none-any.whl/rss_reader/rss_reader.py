"""Main module for working with APP"""

import logging
from config import AppLogger
from rss_parser import RssParser

AppLogger.init_logger('app')
logger = logging.getLogger("app.rss_reader")


def main():
    """Starts APP"""
    rss_parser = RssParser()
    try:
        rss_parser.start()
    except Exception as exc_obj:
        logger.exception(f"Rss reader crashed from {exc_obj}")
        # print(f"Rss reader crashed from {type(exc_obj).__name__}")


if __name__ == "__main__":
    logger.info('RSS reader started working.')
    main()
    logger.info('RSS reader finished working.')
