from .utils import call_api
from .logging_setup import setup_logging
from .input_monitor import start_input_monitor

import logging

# Ensure logging is set up when this package is imported
setup_logging()

# Export common functions and loggers
__all__ = [
    'call_api',
    'start_input_monitor',
    'log_requests',
    'log_data_collector',
    'log_scripts'
]

# Export loggers
log_requests = logging.getLogger('requests')
log_data_collector = logging.getLogger('data_collector')
log_scripts = logging.getLogger('scripts')
