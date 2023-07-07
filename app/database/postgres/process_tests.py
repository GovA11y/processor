# process_tests.py
# Relative Path: app/database/postgres/process_tests.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, select, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from .connect import engine
from .. import logger


Base = declarative_base()


class Rules(Base):  # Description of the Postgres table to extract data from
    __tablename__ = 'rules'
    __table_args__ = {'schema': 'axe'}

    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer)
    rule_type = Column(String(20))
    description = Column(String(250))
    help = Column(String(250))
    help_url = Column(String(250))
    axe_id = Column(String(35))
    impact = Column(String(25))
    tags = Column(JSON)
    nodes = Column(JSON)
    created_at = Column(DateTime(timezone=True))


# Set up session
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


def select_rules_data(new_data_id):
    sql = text("""
        SELECT
               targets.domains.id as domain_id,
               targets.domains.domain,
               targets.urls.id as url_id,
               targets.urls.url,
               axe.rules.scan_id,
               axe.rules.id as rule_id,
               axe.scan_data.scanned_at as tested_at,
               axe.rules.rule_type,
               axe.rules.axe_id,
               axe.rules.impact,
               axe.rules.nodes,
               axe.rules.created_at,
               targets.domains.active
        FROM axe.rules
        LEFT JOIN axe.scan_data ON axe.scan_data.id = axe.rules.scan_id
        LEFT JOIN targets.urls ON targets.urls.id = axe.scan_data.url_id
        LEFT JOIN targets.domains ON targets.domains.id = targets.urls.domain_id
        WHERE axe.rules.id = :rule_id
    """)

    result = session.execute(sql, {'rule_id': new_data_id})

    # Fetch all rows from query
    data = [{column: value for column, value in zip(result.keys(), row)} for row in result.fetchall()]
    # logger.debug(f'Selecting data from Postgres: /n/n{data}')

    session.commit()
    return data


def main():
    # Call the select function
    # For now, we'll just provide an arbitrary ID for testing purposes
    # that matches an ID in your Rules table
    data = select_rules_data(4)
    print(data)  # Print to check selected data


if __name__ == "__main__":
    main()