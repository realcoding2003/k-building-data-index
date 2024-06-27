from .utils import call_api
from .logging_setup import setup_logging

import logging

# Ensure logging is set up when this package is imported
setup_logging()

# Export common functions and loggers
__all__ = [
    'call_api',
    'log_general',
    'log_data_processor',
    'log_collect_all_data'
]

# Export loggers
log_general = logging.getLogger('general')
log_data_processor = logging.getLogger('data_processor')
log_collect_all_data = logging.getLogger('collect_all_data')
