# python3 setup.py sdist

# twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

import random
import tkinter as tk

init = False

def init():
    init = True

def check_init():
    if init == True:
        return True
    else:
        return False
        