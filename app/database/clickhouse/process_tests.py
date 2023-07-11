# process_tests.py
# Relative Path: app/database/clickhouse/process_tests.py
"""
# ClickHouse Process Tests
Inserts Axe A11y tests into ClickHouse from Postgres

"""
from .connect import client as clickhouse_client
import traceback
import json
import html
from datetime import datetime
import uuid
from .. import logger

client = clickhouse_client


def insert_axe_into_clickhouse(data):
    """Inserts data into ClickHouse.

    Args:
        data (list): The list of dictionaries containing the data to be inserted.
    """
    # Prepare the rows as strings
    rows_str = ', '.join([
        f"({row.get('domain_id')}, '{row.get('domain')}', {row.get('url_id')}, '{row.get('url')}', {row.get('scan_id')}, {row.get('rule_id')}, '{row.get('test_id')}', '{row.get('tested_at')}', '{row.get('rule_type')}', '{row.get('axe_id')}', '{row.get('impact')}', '{row.get('target')}', {row.get('html')}, {row.get('failure_summary')}, '{row.get('created_at')}', {row.get('active')}, {row.get('section508')}, {row.get('super_waggy')})"
        for row in data
    ])

    query = f"""
    INSERT INTO axe_tests
    (
        domain_id, domain, url_id, url, scan_id, rule_id, test_id, tested_at, rule_type, axe_id, impact, target, html, failure_summary, created_at, active, section508, super_waggy
    )
    VALUES {rows_str}"""

    try:
        rows_inserted = client.execute(query)
        logger.info(f'{len(data)} rows inserted into ClickHouse')
    except Exception as e:
        # Log the relevant parts of the exception
        exception_traceback = traceback.format_exc()
        # Get the first few rows of data for logging
        first_few_rows = rows_str.split(", ")[:5]
        logger.error(f'First few rows of data:\n{first_few_rows}')
        logger.error(f'Exception: {str(e)}')
        logger.debug(f'Exception Traceback:\n{exception_traceback}')

    # close the client connection
    client.disconnect()
    logger.debug('ClickHouse Connection Closed')

