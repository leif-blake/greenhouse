# Attaches formatting and handlers to logger object
import logging


formatString = '%(levelname)s:%(asctime)s:%(name)s:%(message)s'

# Sets up any logger in same way
def setupLog(logger):
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(formatString)

    # For logging to file
    file_handler = logging.FileHandler('greenhouse.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # For logging to console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(CustomFormatter())

    # Attach to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = "\x1b[38;21m"
    cyan = "\u001b[36m"
    magenta = "\u001b[35m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: magenta + formatString + reset,
        logging.INFO: cyan + formatString + reset,
        logging.WARNING: yellow + formatString + reset,
        logging.ERROR: red + formatString + reset,
        logging.CRITICAL: bold_red + formatString + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)