"""
This file contains the basic configuration for the application.
"""
import logging
import os

global LOGGING_LEVEL
global ROOT_LOGGER


def __setup():
    # Install requirements silently
    os.system("pip install -r requirements.txt --quiet --no-cache-dir")

    # Set logging level
    global LOGGING_LEVEL
    LOGGING_LEVEL = logging.DEBUG

    # Set root logger
    global ROOT_LOGGER
    try:
        if ROOT_LOGGER:
            print("Config already loaded")
            return
    except NameError:
        pass
    ROOT_LOGGER = logging.getLogger(__name__)
    ROOT_LOGGER.setLevel(LOGGING_LEVEL)
    ROOT_LOGGER.addHandler(logging.StreamHandler())
    ROOT_LOGGER.info("Config loaded")
    os.environ["CONFIG_LOADED"] = "True"


if __name__ == "__main__":
    print("This is a configuration file, nothing to run here.")
else:
    # if this package has already been imported, skip
        __setup()
