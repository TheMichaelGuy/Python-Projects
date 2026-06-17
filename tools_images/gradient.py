"""
    gradient.py

    prints a list of colors between two inputs including those colors
"""

from colour import Color # pip install colour
from sys import argv

# importlib execution
def main(*args):
    color1: str = input("Enter hexcode for color1: ")
    color2: str = input("Enter hexcode for color2: ")
    length: int = int(input("Enter length of gradient: "))
    if length < 2:
        length = 2

    colors = list(Color(color1).range_to(Color(color2),length))
    print (colors)

# regular execution
if __name__ == "__main__":

    count : int = len(argv) - 1

    if count < 3:
        print("No command line arguments")
        exit

    color1 = argv[1]
    color2 = argv[2]
    length = int(argv[3])
    if length < 2:
        length = 2

    colors = list(Color(color1).range_to(Color(color2),length))
    print (colors)
