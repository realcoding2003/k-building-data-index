import logging
import os
from datetime import datetime
from src.common.state import LOG_FOLDER, LOG_FOLDER_FORMAT


def setup_logging():
    """Sets up logging configuration for different loggers."""
    # Create log directory with date-time
    log_dir = datetime.now().strftime(f"{LOG_FOLDER}/{LOG_FOLDER_FORMAT}")
    os.makedirs(log_dir, exist_ok=True)

    log_formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # General logger
    requests_logger = logging.getLogger('requests')
    requests_logger.setLevel(logging.INFO)
    requests_handler = logging.FileHandler(os.path.join(log_dir, 'requests.log'))
    requests_handler.setFormatter(log_formatter)
    requests_logger.addHandler(requests_handler)

    # Data Processor logger
    data_processor_logger = logging.getLogger('data_collector')
    data_processor_logger.setLevel(logging.INFO)
    data_processor_handler = logging.FileHandler(os.path.join(log_dir, 'data_collector.log'))
    data_processor_handler.setFormatter(log_formatter)
    data_processor_logger.addHandler(data_processor_handler)

    # Collect All Data logger
    collect_all_data_logger = logging.getLogger('scripts')
    collect_all_data_logger.setLevel(logging.INFO)
    collect_all_data_handler = logging.FileHandler(os.path.join(log_dir, 'scripts.log'))
    collect_all_data_handler.setFormatter(log_formatter)
    collect_all_data_logger.addHandler(collect_all_data_handler)
