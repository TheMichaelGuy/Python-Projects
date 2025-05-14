"""
    clearOutput.py

    Deletes all of the files inside the "output" directory
"""

import glob
import os

# https://www.scaler.com/topics/python/how-to-delete-file-in-python/

for file in glob.glob("output/*"):
    if os.path.isfile(file):
        os.remove(file)
        print("File has been deleted")
    else:
        print("File does not exist")
