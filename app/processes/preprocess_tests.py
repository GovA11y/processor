# preprocess_tests.py
# Relative Path: app/processes/preprocess_tests.py
"""
Preprocesses test data for insertion into ClickHouse
"""

import json
import html
import uuid
from datetime import datetime
from ..utils import logger

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
                "domain": row.get('domain', '') or '',
                "url_id": row.get('url_id', 0),
                "url": row.get('url', '') or '',
                "scan_id": row.get('scan_id', 0),
                "rule_id": row.get('rule_id', 0),
                "test_id": str(uuid.uuid4()),
                "tested_at": format_datetime(row.get('created_at')) or '',
                "rule_type": row.get('rule_type', '') or '',
                "axe_id": row.get('axe_id', '') or '',
                "impact": node.get('impact', '') or '',
                "target": node.get('target', [None])[0] if node.get('target') is not None else '' or '',
                "html": clean_html or '',
                "failure_summary": failure_summary or '',
                "created_at": format_datetime(datetime.now()) or '',
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
    # Check & fix UTF8 issues
    html_string = properly_encode_html(html_string)
    html_string = html_string.strip("'")
    html_string = html.unescape(html_string)
    html_string = html_string.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    html_string = html_string.translate({ord(i): None for i in '\0'})
    return repr(html_string)


def properly_encode_html(html_string):
    try:
        html_string.encode('utf-8')
    except UnicodeEncodeError:
        logger.debug('String is NOT UTF8, fixing...')
        # Replace invalid characters with a replacement character
        html_string = html_string.encode('utf-8', errors='replace').decode('utf-8')
    return html_string


def format_datetime(dt):
    """Formats a datetime object.

    Args:
        dt (datetime): The datetime object to be formatted.

    Returns:
        datetime: The formatted datetime.
    """
    if dt is not None:
        return dt
    else:
        return None
