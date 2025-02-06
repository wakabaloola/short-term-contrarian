# src/utils/logger.py

import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime

class ProjectLogger:
    """Centralised logging configuration for the project.

    Overview:
    ---------

    - Centralized Configuration: All logging settings are managed in one place (src/utils/logger.py)
    - Hierarchical Logging: Uses Python's logging hierarchy with module-specific loggers
    - Multiple Outputs:
        * Console output for INFO and above (for immediate feedback)
        * File output for DEBUG and above (for detailed troubleshooting)
    - Rotating Log Files: Automatically manages log file size and keeps backup files
    - Consistent Format:
        * File logs: Include timestamp, logger name, level, file location, and message
        * Console logs: Simpler format for readability

    How to use:
    -----------

    - Create the logger.py file in your utils directory
    - Import and use the logger in your modules as shown in the example:
            
            # Example usage in src/data_acquisition/get_symbols.py
            from src.utils.logger import get_logger

            logger = get_logger(__name__)

            def fetch_symbols():
                try:
                    logger.info("Starting symbol fetch process")
                    logger.debug("Connecting to data source")
                    
                    # Your code here
                    symbols = ["AAPL", "GOOGL"]
                    
                    logger.info(f"Successfully fetched {len(symbols)} symbols")
                    return symbols
                except Exception as e:
                    logger.error(f"Error fetching symbols: {str(e)}", exc_info=True)
                    raise

    - Logs will be stored in a logs directory at your project root

    Logging levels:
    ---------------

    - DEBUG: Detailed information for debugging
    - INFO: General information about program execution
    - WARNING: Indicate a potential problem
    - ERROR: A more serious problem
    - CRITICAL: Program may not be able to continue

    You can adjust the logging levels, formats, and file rotation settings in the ProjectLogger class to match your needs. The current setup will create log files with names like project_20250206.log and rotate them when they reach 10MB.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        

    def __init__(self, log_dir="logs"):
        """
        Initialize logger with custom configuration.
        
        Args:
            log_dir (str): Directory to store log files
        """
        if hasattr(self, 'initialized'):
            return
        self.initialized = True

        # Create logs directory if it doesn't exist
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s'
        )
        
        # Create handlers
        # Rotating file handler - creates new file when size limit is reached
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / f"project_{datetime.now().strftime('%Y_%m_%d')}.log",
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)
        
        # Create root logger
        self.root_logger = logging.getLogger()
        self.root_logger.setLevel(logging.DEBUG)
        
        # Remove any existing handlers
        self.root_logger.handlers.clear()
        
        # Add handlers
        self.root_logger.addHandler(file_handler)
        self.root_logger.addHandler(console_handler)
    
    def get_logger(self, name):
        """Get a logger with the specified name.
        
        Args:
            name (str): Name for the logger, typically __name__
            
        Returns:
            logging.Logger: Configured logger instance
        """
        return logging.getLogger(name)

# Default logger instance
project_logger = ProjectLogger()
get_logger = project_logger.get_logger

