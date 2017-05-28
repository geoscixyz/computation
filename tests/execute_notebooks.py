import nbformat
from nbconvert.preprocessors import ClearOutputPreprocessor
import os
import sys

dirname, _ = os.path.split(os.path.abspath(__file__))
nbdir = os.path.sep.join(dirname.split(os.path.sep)[:-1] + ['docs'])


def clearNbOutput():
    cwd = os.getcwd()
    # walk the test directory and find all notebooks
    for dirname, dirnames, filenames in os.walk(nbdir):
        if dirname != ".ipynb_checkpoints":
            for filename in filenames:
                if (
                    filename.endswith(".ipynb") and not
                    filename.endswith("-checkpoint.ipynb")
                ):
                    with open(os.path.join(dirname, filename)) as f:
                        print("Clearing output from {}".format(filename))
                        nb = nbformat.read(f, as_version=4)
                        ep = ClearOutputPreprocessor()
                        ep.preprocess(nb, {})
                        print("   ... done\n")
    return True

if __name__ == '__main__':
    clearNbOutput()
