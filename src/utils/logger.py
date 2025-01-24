import logging
import os
from pathlib import Path

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up and returns a logger with the specified name.
    
    Args:
        name (str): Name of the logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Get the project root directory (where src is located)
    project_root = Path(__file__).parent.parent.parent
    
    # Create logs directory in project root
    logs_dir = project_root / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    # Configure log file path
    log_file = logs_dir / 'app.log'
    
    # Set up logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers
    if not logger.handlers:
        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(log_file)

        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.DEBUG)

        # Create formatters and add to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger
