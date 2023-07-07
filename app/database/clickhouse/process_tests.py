# process_tests.py
# Relative Path: app/database/clickhouse/process_tests.py
"""
# ClickHouse Process Tests
Inserts Axe A11y tests into ClickHouse from Postgres

"""
from .connect import client as clickhouse_client
import json
from datetime import datetime
import uuid
from .. import logger

client = clickhouse_client


def insert_axe_into_clickhouse(data):
    """Inserts data into ClickHouse.

    Args:
        data (list): The list of tuples containing the data to be inserted.
    """
    # and then for each row in your data...
    for row in data:
        # logger.debug(f'Inserting data into ClickHouse: /n/n{data}')

        # this gives current datetime
        now = datetime.now()
        # this is of String type and gives string in the 'YYYY-MM-DD hh:mm:ss' format
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        created_at = f"'{now_str}'"

        # parse JSON in 'nodes' column
        nodes = row['nodes'] if isinstance(row['nodes'], list) else json.loads(row['nodes'])
        # for every 'node' in 'nodes' do an individual insert
        for node in nodes:

            # Here we make manual adjustments to extract values from the JSON object
            # like 'target', 'html', 'failureSummary'
            # and ensure that other values are correctly formatted for insertion
            failure_summary = f"'{node.get('failureSummary')}'" if node.get('failureSummary') is not None else "NULL"
            # Use `row` object to get `created_at`
            if row.get('created_at') is not None:
                tested_at = f"'{row.get('created_at').strftime('%Y-%m-%d %H:%M:%S')}'"
            else:
                tested_at = "NULL"


            query = f"""
            INSERT INTO axe_tests
            (
                domain_id, domain, url_id, url, scan_id, rule_id, test_id, tested_at, rule_type, axe_id, impact, target, html, failure_summary, created_at, active, section508, super_waggy
            )
            VALUES (
                {row.get('domain_id', 0)}, '{row.get('domain', '')}', {row.get('url_id', 0)}, '{row.get('url', '')}',
                {row.get('scan_id', 0)}, {row.get('rule_id', 0)}, '{uuid.uuid4()}', {tested_at},
                '{row.get('rule_type', '')}', '{row.get('axe_id', '')}', '{node.get('impact', '')}',
                '{node.get('target', [None])[0] if node.get('target') is not None else ''}',
                '{node.get('html', '')}', {failure_summary}, {created_at},
                {row.get('active', 1)},
                {row.get('section508', 0)}, {row.get('super_waggy', 0)}
            )"""
            client.execute(query)
            # logger.debug(f'Executing Clickhouse Query: {query}')

    # close the client connection
    client.disconnect()
    logger.debug('ClickHouse Connection Closed')