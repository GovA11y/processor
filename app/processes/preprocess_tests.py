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
        try:
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

                # Select the first target...
                target = process_target(node.get('target', ['']), row, node)

                # Replace None with default values
                preprocessed_row = {
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
                    "target": target,  # Use the selected target here.
                    "html": clean_html,
                    "failure_summary": failure_summary,
                    "created_at": format_datetime(datetime.now()),
                    "active": row.get('active', 1),
                    "section508": row.get('section508', 0),
                    "super_waggy": row.get('super_waggy', 0)
                }
                for key, value in preprocessed_row.items():
                    if value is None:
                        preprocessed_row[key] = ''

                preprocessed_data.append(preprocessed_row)

        except Exception as e:
                logger.error(f"Error while processing row: {row}")
                logger.error(f"Node: {node}")
                logger.error(f"Exception: {str(e)}")
                continue  # skip to the next row

    return preprocessed_data



def process_target(target, row, node):
    """
    Process the target value.
    If the target is a list with all same values, return the single value.
    If the target is a list with different values, log the message and return the first value.
    If the target is None, return an empty string.
    If the target is a single value, return the value.
    """
    if isinstance(target, list):
        # Flatten the list if it contains sublists
        flat_target = [item for sublist in target for item in sublist] if all(isinstance(sub, list) for sub in target) else target
        if len(flat_target) == 0:
            return ''
        elif len(set(flat_target)) > 1:  # set(flat_target) creates a set, which removes duplicates
            logger.warning(f"DUPLICATE TARGET: {row['url_id']}, {row['rule_id']}, {row['scan_id']}, {format_datetime(row.get('created_at'))}, {row.get('axe_id')}")
            return flat_target[0]
        else:
            return flat_target[0]
    elif target is None:
        return ''
    else:
        return target


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
    if html_string is None:
        return repr("NULL")

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
