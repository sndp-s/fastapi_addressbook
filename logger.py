"""
Custom Formatted logger
"""
import logging
import sys


def setup_logger():
    """
    Formatted logger

    This is a basic formatted logger

    In real world system we would format the logger based on our monitoring system format,
    for example: OpenSearch

    I would also have a tracing mechanism to track the request across various function calls
    """
    # Create a logger
    _logger = logging.getLogger("address_book_logger")
    _logger.setLevel(logging.DEBUG)

    # Create handlers
    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = logging.FileHandler("address_book_api.log")
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    _logger.addHandler(c_handler)
    _logger.addHandler(f_handler)

    return _logger


logger = setup_logger()
