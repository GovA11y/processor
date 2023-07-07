"""
test_logger.py

This module contains unit tests for the logger module.

Author: TheBoatyMcBoatFace
"""

import unittest
from unittest.mock import patch, MagicMock
import logging
import time
import sys
import os

# Append the parent directory to the sys path to import the logger module correctly
sys.path.append(os.path.abspath('.'))

from app import logger


class LoggerTest(unittest.TestCase):
    """
    Unit tests for the logger module.
    """

    def setUp(self):
        """
        Set up the test case.

        This method creates a stream handler to capture the log output.
        """
        # Create a stream handler to capture the log output
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logging.DEBUG)
        self.log_output = []

        def capture_logs(record):
            self.log_output.append(record.getMessage())

        self.stream_handler.setFormatter(logging.Formatter('%(message)s'))
        self.stream_handler.emit = capture_logs

        # Add the stream handler to the logger
        logger.addHandler(self.stream_handler)

    def tearDown(self):
        """
        Clean up after the test case.

        This method removes the stream handler from the logger.
        """
        # Remove the stream handler from the logger
        logger.removeHandler(self.stream_handler)

    def test_logger_output(self):
        """
        Test the logger output.

        This method logs some messages and asserts that the captured log messages match the expected output.
        """
        # Log some messages
        logger.debug('This is a debug message')
        logger.info('This is an info message')
        logger.warning('This is a warning message')
        logger.error('This is an error message')
        logger.critical('This is a critical message')

        # Assert the captured log messages
        expected_output = [
            'This is a debug message',
            'This is an info message',
            'This is a warning message',
            'This is an error message',
            'This is a critical message'
        ]
        self.assertEqual(self.log_output, expected_output)


if __name__ == '__main__':
    unittest.main()
