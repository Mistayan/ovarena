"""
This file contains the basic configuration for the application.
"""
import logging
import os

import colorama

PROJECT_NAME = "ovarena"
__workdir__ = os.path.dirname(os.path.abspath(__file__))
__rootdir__ = os.path.dirname(__workdir__)
colorama.init()

LOGGING_LEVEL = logging.INFO
ROOT_LOGGER = None


def __setup():
    # Install requirements silently
    os.system(f"pip install -r {__workdir__}/requirements.txt --quiet --no-cache-dir")

    # Set logging level
    global LOGGING_LEVEL
    LOGGING_LEVEL = logging.DEBUG
    logging.basicConfig(level=LOGGING_LEVEL,
                        format=f"{colorama.Fore.RED}%(levelname)s -%(asctime)s -"
                               f" {colorama.Fore.GREEN}%(name)s -"
                               f" {colorama.Fore.YELLOW} %(message)s")
    # format="%(levelname)s -%(asctime)s - %(name)s - %(message)s")

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
