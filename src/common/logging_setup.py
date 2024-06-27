import logging
import os
from datetime import datetime


def setup_logging():
    """Sets up logging configuration for different loggers."""
    # Create log directory with date-time
    log_dir = datetime.now().strftime('logs/%Y-%m-%d_%H-%M-%S')
    os.makedirs(log_dir, exist_ok=True)

    log_formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # General logger
    general_logger = logging.getLogger('general')
    general_logger.setLevel(logging.INFO)
    general_handler = logging.FileHandler(os.path.join(log_dir, 'general.log'))
    general_handler.setFormatter(log_formatter)
    general_logger.addHandler(general_handler)

    # Data Processor logger
    data_processor_logger = logging.getLogger('data_processor')
    data_processor_logger.setLevel(logging.INFO)
    data_processor_handler = logging.FileHandler(os.path.join(log_dir, 'data_processor.log'))
    data_processor_handler.setFormatter(log_formatter)
    data_processor_logger.addHandler(data_processor_handler)

    # Collect All Data logger
    collect_all_data_logger = logging.getLogger('collect_all_data')
    collect_all_data_logger.setLevel(logging.INFO)
    collect_all_data_handler = logging.FileHandler(os.path.join(log_dir, 'collect_all_data.log'))
    collect_all_data_handler.setFormatter(log_formatter)
    collect_all_data_logger.addHandler(collect_all_data_handler)

    # Add console handler to all loggers
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    general_logger.addHandler(console_handler)
    data_processor_logger.addHandler(console_handler)
    collect_all_data_logger.addHandler(console_handler)
