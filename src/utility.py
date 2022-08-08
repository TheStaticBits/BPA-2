import logging

def setup_logger():
    """ Setup the Python logger for use """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%([%(levelname)s] %(module)s: %(message)s")
    
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
