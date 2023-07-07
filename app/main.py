# main.py
# Relative Path: app/main.py
"""
# Main Controller of GovA11y Data Processing

"""
import time
from .processes import execute_axes
from .database import fetch_unprocessed_rules, mark_axe_rule_as_processed

# rule_id = 15
# 1363


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