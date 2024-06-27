from .utils import call_api, create_directory_if_not_exists
from .logging_setup import setup_logging
from .state import stop_event

import logging

# Ensure logging is set up when this package is imported
setup_logging()

# Export common functions and loggers
__all__ = [
    'call_api',
    'create_directory_if_not_exists',
    'setup_logging',
    'stop_event',
    'general_logger',
    'data_processor_logger',
    'collect_all_data_logger'
]

# Export loggers
general_logger = logging.getLogger('general')
data_processor_logger = logging.getLogger('data_processor')
collect_all_data_logger = logging.getLogger('collect_all_data')
