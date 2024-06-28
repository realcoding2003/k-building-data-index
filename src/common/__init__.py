from .utils import call_api
from .logging_setup import setup_logging

import logging

# Ensure logging is set up when this package is imported
setup_logging()

# Export common functions and loggers
__all__ = [
    'call_api',
    'log_general',
    'log_data_collector',
    'log_scripts'
]

# Export loggers
log_general = logging.getLogger('general')
log_data_collector = logging.getLogger('data_collector')
log_scripts = logging.getLogger('scripts')
