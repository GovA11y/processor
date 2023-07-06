# process_tests.py
# Relative Path: app/database/postgres/process_tests.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from .connect import engine


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
    created_at = Column(DateTime(timezone=True), default=func.now())


# Set up session
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


def select_rules_data(new_data_id):
    rules_row = select(
        Rules.id,
        Rules.scan_id,
        Rules.rule_type,
        Rules.description,
        Rules.help,
        Rules.help_url,
        Rules.axe_id,
        Rules.impact,
        Rules.tags,
        Rules.nodes,
        Rules.created_at,
    ).where(Rules.id == new_data_id)

    result = session.execute(rules_row)
    return result.fetchall()  # This will return a list of tuples


def main():
    # Call the select function
    # For now, we'll just provide an arbitrary ID for testing purposes
    # that matches an ID in your Rules table
    data = select_rules_data(4)
    print(data)  # Print to check selected data


if __name__ == "__main__":
    main()