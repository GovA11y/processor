# fetch_unprocessed.py
# Relative Path: app/database/postgres/fetch_unprocessed.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .connect import engine
from .. import logger

# Set up session
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


def fetch_unprocessed_rules(limit=10000, offset=0):
    """Fetches unprocessed rule_id from Postgres with limit and offset."""
    rule_limit = int(os.environ.get('RULE_LIMIT', limit))
    rule_offset = int(os.environ.get('RULE_OFFSET', offset))

    result = session.execute(text("""
        SELECT id as rule_id
        FROM axe.rules
        WHERE imported = false
        ORDER BY id
        LIMIT :rule_limit OFFSET :rule_offset
    """), {'rule_limit': rule_limit, 'rule_offset': rule_offset})

    logger.info(f'Importing {rule_limit} unprocessed rules from Postgres with offset {rule_offset}')

    # Fetch all records from the query execution result
    records = result.fetchall()

    # Iterate and create a list containing 'rule_id' from each record
    rule_ids = [record.rule_id for record in records]

    session.close()

    return rule_ids
