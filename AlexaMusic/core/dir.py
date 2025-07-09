
from os import listdir, mkdir
from os.path import isdir
from shutil import rmtree

from ..logging import LOGGER


def dirr():
    current_items = listdir()

    if "assets" not in current_items:
        LOGGER(__name__).warning(
            "Assets Folder not Found. Please clone repository again."
        )
        exit()

    for folder in ("downloads", "cache"):
        if folder in current_items and isdir(folder):
            rmtree(folder)
        mkdir(folder)

    LOGGER(__name__).info("Directories Updated.")
