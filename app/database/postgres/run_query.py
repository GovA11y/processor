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

    if vars:
        formatted_sql_content = text(sql_content) % tuple(vars)
    else:
        formatted_sql_content = text(sql_content)

    logger.info(f"Running query: {query_name}")

    session = conn()

    try:
        result = session.execute(formatted_sql_content)
        session.commit()

        if re.match(r"(SELECT|UPDATE)", sql_content, re.IGNORECASE):
            rows = result.fetchall()
            logger.debug(f"Result rows: {rows}")
            return rows
        else:  # For INSERT, DELETE or any other query type
            logger.info(f"Affected rows: {result.rowcount}")
            return {"affected_rows": result.rowcount}

    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Error while running query {query_name}: {str(e)}")
        return None
    finally:
        session.close()
