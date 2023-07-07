# process_tests.py
# Relative Path: app/database/clickhouse/process_tests.py
"""
# ClickHouse Process Tests
Inserts Axe A11y tests into ClickHouse from Postgres

"""
from .connect import client as clickhouse_client
import json
from .. import logger

client = clickhouse_client


def insert_axe_into_clickhouse(data):
    """Inserts data into ClickHouse.

    Args:
        data (list): The list of tuples containing the data to be inserted.
    """
    # and then for each row in your data...
    for row in data:

        # parse JSON in 'nodes' column
        nodes = json.loads(row['nodes'])
        # for every 'node' in 'nodes' do an individual insert
        for node in nodes:

            # Here we make manual adjustments to extract values from the JSON object
            # like 'target', 'html', 'failureSummary'
            # and ensure that other values are correctly formatted for insertion

            query = f"""
            INSERT INTO tests
            (
                id, scan_id, rule_type,
                description, help, help_url,
                axe_id, impact, tags,
                target, html, failure_summary,
                created_at
            )
            VALUES (
                {row['id']}, {row['scan_id']},'{row['rule_type']}',
                '{row['description']}', '{row['help']}', '{row['help_url']}',
                '{row['axe_id']}', '{row['impact']}', '{row['tags']}',
                '{node['target']}', '{node['html']}', '{node['failureSummary']}',
                '{row['created_at']}'
            )"""
            client.execute(query)
            logger.debug(f'Executing Clickhouse Query: {query}')

    # close the client connection
    client.disconnect()
    logger.debug('ClickHouse Connection Closed')