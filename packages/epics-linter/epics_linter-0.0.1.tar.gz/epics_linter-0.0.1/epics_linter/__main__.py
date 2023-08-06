import sys
from epics_linter.linter import Linter

if __name__ == "__main__":
    with open(sys.argv[1], "r") as file:
        linter = Linter()
        linter.lint(file.read())
