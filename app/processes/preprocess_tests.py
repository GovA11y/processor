# preprocess_tests.py
# Relative Path: app/processes/preprocess_tests.py
"""
Preprocesses test data for insertion into ClickHouse
"""

import json
import html
import uuid
from datetime import datetime

def preprocess_data(data):
    """Preprocesses data for insertion into ClickHouse.

    Args:
        data (list): The list of tuples containing the data to be preprocessed.

    Returns:
        list: The list of preprocessed tuples ready for insertion.
    """
    preprocessed_data = []

    for row in data:
        # Parse JSON in 'nodes' column
        nodes = row['nodes'] if isinstance(row['nodes'], list) else json.loads(row['nodes'])
        # For every 'node' in 'nodes' do an individual insert
        if not nodes:
            nodes = [{}]
        for node in nodes:
            # Sanitize Failure Summary Data
            failure_summary = sanitize_failure_summary(node.get('failureSummary'))

            # Get & Sanitize html
            clean_html = sanitize_html(node.get('html'))

            # Preprocess data and append to preprocessed_data
            preprocessed_data.append({
                "domain_id": row.get('domain_id', 0),
                "domain": row.get('domain', ''),
                "url_id": row.get('url_id', 0),
                "url": row.get('url', ''),
                "scan_id": row.get('scan_id', 0),
                "rule_id": row.get('rule_id', 0),
                "test_id": str(uuid.uuid4()),
                "tested_at": format_datetime(row.get('created_at')),
                "rule_type": row.get('rule_type', ''),
                "axe_id": row.get('axe_id', ''),
                "impact": node.get('impact', ''),
                "target": node.get('target', [None])[0] if node.get('target') is not None else '',
                "html": clean_html,
                "failure_summary": failure_summary,
                "created_at": format_datetime(datetime.now()),
                "active": row.get('active', 1),
                "section508": row.get('section508', 0),
                "super_waggy": row.get('super_waggy', 0)
            })

    return preprocessed_data


def sanitize_failure_summary(failure_summary):
    """Sanitizes the failure summary data.

    Args:
        failure_summary (str): The failure summary data to be sanitized.

    Returns:
        str: The sanitized failure summary data.
    """
    if failure_summary is not None:
        failure_summary = failure_summary.replace('\n', ' ')
        failure_summary = failure_summary.replace('\0', '')
    else:
        failure_summary = "NULL"
    return repr(failure_summary)


def sanitize_html(html_string):
    """Sanitizes the html data.

    Args:
        html_string (str): The html data to be sanitized.

    Returns:
        str: The sanitized html data.
    """
    html_string = html_string if html_string is not None else "NULL"
    html_string = html_string.strip("'")
    html_string = html.unescape(html_string)
    html_string = html_string.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    html_string = html_string.translate({ord(i): None for i in '\0'})
    return repr(html_string)


def format_datetime(dt):
    """Formats a datetime object into a string.

    Args:
        dt (datetime): The datetime object to be formatted.

    Returns:
        str: The formatted datetime string.
    """
    if dt is not None:
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return "NULL"
