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
from ..database import axe_postgres, axe_clickhouse
from ..utils import logger


# define how to get data from postgres
def get_axes(new_data_id):
    data = axe_postgres(new_data_id)
    # logger.debug(f'{data}')
    return data


# define how to put data into ClickHouse
def throw_axes(data):
    axe_clickhouse(data)


# for executing both functions in sequence
def execute_axes(new_data_id):
    data = get_axes(new_data_id)
    throw_axes(data)
    logger.debug('Inserting into Clickhouse')