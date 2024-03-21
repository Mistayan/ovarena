# -*- coding: utf-8 -*-
"""
Created by: Mistayan
Project: President-Game
IDE: PyCharm
Creation-date: 11/26/22
Purpose: Create a venv and install requirements
"""

import os
import sys
from subprocess import Popen

ENV_DIR = "venv"
BASEDIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = "Scripts" if "win" in sys.platform.lower() else "bin"
VENV_PYTHON = os.path.join(BASEDIR, ENV_DIR, LIB_DIR, "python")

if __name__ == "__main__":
    if not os.path.exists(os.path.join(BASEDIR, "venv")) and \
            not os.path.exists(os.path.join(BASEDIR, "venv", "bin")) \
            or sys.argv.__contains__("--setup"):
        print(f"Creating virtual environment : {ENV_DIR}")
        # communicate, so we know what happens
        init = Popen(f"python -m venv {ENV_DIR}".split()).communicate()  # <==
    print("Upgrading pip and wheel")
    check_pip_wheel = Popen(f"{VENV_PYTHON} -m pip install --upgrade pip wheel".split()).communicate()
    print("Applying requirements ...")
    install = Popen(f"{VENV_PYTHON} -m pip install -r requirements.txt".split()).communicate()
