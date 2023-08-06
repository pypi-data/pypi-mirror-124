"""Storage module with settings for argparse and logging"""

import argparse
import logging
import sys
from enum import Enum


class AppConstant(Enum):
    """Class immutable values"""
    ACTUAL_VERSION = 'Version 1.0.0'


class AppArgParser:
    """Class for initializing arguments for working with CLI"""

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
        self.parser.add_argument('--version', action="version", version=AppConstant.ACTUAL_VERSION.value,
                                 help='Print version info')
        self.parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
        self.parser.add_argument('--verbose', action="store_true", help='Outputs verbose status messages')
        self.parser.add_argument('--limit', type=int, default=None, help='Limit news topics if this parameter provided')
        self.parser.add_argument('source', type=str, help='URL RSS')

    def get_args(self) -> argparse.Namespace:
        """
        Initialization of arguments
        :return: object for storing attributes
        """
        return self.parser.parse_args()


class AppLogger:
    """Class for initialization and setup logger and handlers"""

    FORMAT = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'

    @staticmethod
    def init_logger(name):
        """Initialization and setup root logger. Setup and start file handler"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(filename='mylogs.log', mode='w', encoding='utf-8')
        fh.setFormatter(logging.Formatter(AppLogger.FORMAT))
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

    @staticmethod
    def activate_verbose():
        """Setup and start stream handler for verbose mode"""
        logger = logging.getLogger('app')
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(logging.Formatter(AppLogger.FORMAT))
        sh.setLevel(logging.INFO)
        logger.addHandler(sh)