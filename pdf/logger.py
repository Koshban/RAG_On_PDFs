import os
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_logger(name):
    """
    Returns a logger with the specified name, configured to log to a central file.

    Args:
        name (str): The name of the logger (usually the module name).

    Returns:
        logging.Logger: A configured logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the desired logging level

    # Create a file handler and set the logging format
    file_handler = logging.FileHandler(os.path.join(BASE_DIR, "application.log"))
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    return logger