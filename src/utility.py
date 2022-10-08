import logging
import json

def load_constants():
    """ Loads constants file for constant data values within the game """
    with open("data/constants.json") as f:
        return json.load(f)


def setup_logger(constants):
    """ Setup the Python logger for use """
    logger = logging.getLogger("")
    
    # Set level based on what is set in constants JSON file
    if   (constants["log"]["level"] == "DEBUG"):   logger.setLevel(logging.DEBUG)
    elif (constants["log"]["level"] == "WARNING"): logger.setLevel(logging.WARNING)
    else:                                          logger.setLevel(logging.INFO)

    fileFormatter =    logging.Formatter("[%(asctime)s] - [%(levelname)s] %(name)s: %(message)s")
    consoleFormatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    
    fileHandler =    logging.FileHandler(constants["log"]["output"])
    consoleHandler = logging.StreamHandler()

    fileHandler.setFormatter(fileFormatter)
    consoleHandler.setFormatter(consoleFormatter)

    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)