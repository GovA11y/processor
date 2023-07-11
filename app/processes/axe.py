# axe.py
# Relative Path: app/processes/axe.py
"""
# Axe Test Results Controller
Manages selecting and monitoring Postgres for Rules
and copying over to ClickHouse

## Steps
    1) Trigger app/database/postgres/process_tests.py and select data
    2) Send data to app/database/clickhouse/process_tests.py
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from ..database import axe_postgres, axe_clickhouse
from ..utils import logger
from .preprocess_tests import preprocess_data


# define how to get data from postgres
def get_axes(new_data_id):
    data = axe_postgres(new_data_id)
    return data

# define how to preprocess data
def preprocess_axes(data):
    preprocessed_data = preprocess_data(data)
    return preprocessed_data

# define how to put data into ClickHouse
def throw_axes(data):
    axe_clickhouse(data)

# for executing both functions in sequence
def execute_axes(new_data_id):
    data = get_axes(new_data_id)
    preprocessed_data = preprocess_axes(data)  # preprocess the data
    throw_axes(preprocessed_data)
    logger.debug('Inserting into Clickhouse')