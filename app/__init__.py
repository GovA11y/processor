# app/__init__.py
from .utils import configure_monitoring, logger
from dotenv import load_dotenv

from .database.postgres.connect import test_connection

from .processes import start_processes

def startup():
    logger.info('Starting up...')
    load_dotenv()
    configure_monitoring()
    test_connection()
    start_processes()

