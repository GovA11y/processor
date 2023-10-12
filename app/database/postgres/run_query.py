# app/database/postgres/run_query.py
import os
import re
from app.database.postgres.connect import postgres_conn as conn
from app import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

QUERIES_DIRECTORY = os.path.join(os.path.dirname(__file__), "queries")

def run_query(query_name, vars=None):
    query_file = os.path.join(QUERIES_DIRECTORY, f"{query_name}.sql")

    with open(query_file) as file:
        sql_content = file.read()

    logger.info(f"Running query: {query_name}")

    session = conn()

    try:
        result = session.execute(text(sql_content), vars)
        logger.debug(f'Formatted SQL to Run:\n %s', sql_content)

        session.commit()

        rows = result.fetchall()
        logger.debug(f"Result rows: {rows}")

        return rows

    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Error while running query {query_name}: {str(e)}")
        return None
    finally:
        session.close()
