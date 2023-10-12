# app/processes/__init__.py

# from .axe import get_axes, execute_axes
# from .preprocess_tests import preprocess_data

from .naked_urls import find_nakies
from app import logger

def start_processes():
    logger.info('Starting processes...')
    find_nakies()
