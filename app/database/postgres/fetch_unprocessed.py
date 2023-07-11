# fetch_unprocessed.py
# Relative Path: app/database/postgres/fetch_unprocessed.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .connect import engine
from .. import logger

# Set up session
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


def fetch_unprocessed_rules(limit=10):
    """Fetches all rule_id that are not processed yet."""
    result = session.execute(text("""
        SELECT id as rule_id
        FROM axe.rules
        WHERE imported = false
        LIMIT :limit
     """), {'limit': limit})
    logger.info(f'Importing {limit} unprocessed rules from Postgres')

    # Fetch all records from the query execution result
    records = result.fetchall()

    # Iterate and create a list containing 'rule_id' from each record
    rule_ids = [record.rule_id for record in records]

    session.close()

    return rule_ids