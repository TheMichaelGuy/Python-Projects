"""
    gradient.py

    prints a list of colors between two inputs including those colors
"""

from colour import Color
from sys import argv

count : int = len(argv) - 1

if count < 3:
    print("No command line arguments")
    exit

color1 = argv[1]
color2 = argv[2]
length = int(argv[3])
if length < 2:
    lenght = 2

colors = list(Color(color1).range_to(Color(color2),length))
print (colors)
