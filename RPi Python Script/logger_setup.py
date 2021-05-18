# Attaches formatting and handlers to logger object
import logging


# Sets up any logger in same way
def setupLog(logger):
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

    # For logging to file
    file_handler = logging.FileHandler('greenhouse.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # For logging to console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Attach to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)