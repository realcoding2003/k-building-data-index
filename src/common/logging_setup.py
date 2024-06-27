import logging


def setup_logging(log_file):
    """Sets up logging configuration."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='[%(asctime)s %(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.getLogger().addHandler(logging.StreamHandler())
