# app/main.py
import time
import sys
import os
from .utils import logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.processes import execute_axes
from app.database import fetch_unprocessed_rules, mark_axe_rule_as_processed

def yeet_axes():
    while True:
        rules_to_process = fetch_unprocessed_rules()
        if rules_to_process:
            # When there are rule_ids to process, process them.
            for rule_id in rules_to_process:
                execute_axes(rule_id)  # Inserts into ClickHouse
                mark_axe_rule_as_processed(rule_id)  # Marks as processed in Postgres
        else:
            # When there are no more rule_ids to process, sleep for 10 seconds before checking again.
            time.sleep(10)


if __name__ == "__main__":
    yeet_axes()
