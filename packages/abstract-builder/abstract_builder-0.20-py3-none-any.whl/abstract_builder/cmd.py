import subprocess
import sys
import os

from abstract_builder import main


def build_command():
    args = sys.argv[1:]

    if len(args) < 1:
        print("Недопустимый формат ввода")
        return

    root_catalog = args[0]

    main.build(root_catalog)

