"""
A collection of some python library/project specific utilities.
Possibly more generic ones to follow
"""
import glob
import os
import shutil


def cleanBuilds() -> bool:
    """
    Finds common build/dist fdlders and removes them recursively from the base
    of the project, where 'tasks.py' is
    """

    def removeFolder(path: str) -> None:
        root = "./"
        shutil.rmtree(os.path.join(root, path), ignore_errors=True)

    removeFolder("dist")
    removeFolder("build")

    ret = glob.glob("*egg-info")
    if len(ret) > 0:
        removeFolder(ret[0])

    # As taskr tasks return true or false for status
    return True


def cleanCompiles() -> bool:
    """
    Finds compiled (.pyc) files and removes them recursively from the base
    of the project, where 'tasks.py' is
    """
    for root, dirs, files in os.walk(".", topdown=False):
        if "__pycache__" in dirs:
            shutil.rmtree(os.path.join(root, "__pycache__"))
        for name in files:
            if ".pyc" in name:
                os.remove(os.path.join(root, name))

    # As taskr tasks return true or false for status
    return True


def inVenv() -> bool:
    """
    Let's you know if you're in a virtual environment or not.
    """
    return not os.environ.get("VITRUAL_ENVIRON") is None
