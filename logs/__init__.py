import logging
import sys

root = logging.getLogger()
# log_level = current_app.config.get('LOG_LEVEL', 'INFO').upper() 

log_level = 'INFO'

root.setLevel(log_level)
root.propagate = False

# Add StreamHandler for local output
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(process)d %(thread)d %(asctime)s [%(name)s][%(levelname)s]::%(message)s')
stream_handler.setFormatter(formatter)
root.addHandler(stream_handler)

# Logging utility functions
def log(message, *args, **kwargs):
    """
    Log an info level message to stdout.
    
    :param message: The message to log
    """
    logging.info(message, *args, **kwargs)

def log_error(message, *args, **kwargs):
    """
    Log an error level message to stdout.
    
    :param message: The message to log
    """
    logging.error(message, *args, **kwargs)

def log_exception(message, *args, **kwargs):
    """
    Log an exception (with traceback) to stdout.
    
    :param message: The message to log
    """
    logging.exception(message, *args, **kwargs)

def debug(message, *args, **kwargs):
    """
    Log a debug level message to stdout.
    
    :param message: The message to log
    """
    logging.debug(message, *args, **kwargs)
