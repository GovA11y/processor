# app/processes/__init__.py
import time
from multiprocessing import Process
from app import logger

# Process Imports
from .naked_urls import find_nakies

def process_loop(process_func, sleep_time):
    while True:
        if not process_func():  # If there is no data to process
            time.sleep(sleep_time)  # Wait for the specified amount of time


def start_processes():
    logger.info('Starting processes...')

    # Functions with their sleep times
    processes = [
        (find_nakies, 30)
        #(fix_axe, 60)
    ]

    for process_func, sleep_time in processes:
        process = Process(target=process_loop, args=(process_func, sleep_time))
        process.start()
