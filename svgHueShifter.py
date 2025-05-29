"""
    svgHueShifter.py

    Alters colors of svg documents by locating hex codes and changing the colors based on the hue desired
    This is meant for svg sprites created in Scratch and relies on its use of hexCodes for coloring. This will not work for other documents
"""

import colorsys
import os
import sys

def hexToRGB(hexCode : str):
    if len(hexCode) != 6:
        return
    
    red = int(hexCode[0:2],16)
    green = int(hexCode[2:4],16)
    blue = int(hexCode[4:],16)
    return red, green, blue

def RGBToHex(red : int, green : int, blue : int):
    R = str(hex(red))[2:]
    G = str(hex(green))[2:]
    B = str(hex(blue))[2:]
    if len(R) == 1:
        R = "0" + R
    if len(G) == 1:
        G = "0" + G
    if len(B) == 1:
        B = "0" + B
    return str(R + G + B)

def hueShifter(hexCode : str, hueOffset : float):
    if len(hexCode) != 6 or hueOffset < 0 or hueOffset > 1:
        return
    R,G,B = hexToRGB(hexCode)
    R /= 255
    G /= 255
    B /= 255
    H,S,V = colorsys.rgb_to_hsv(R,G,B)
    H += hueOffset
    if H > 1:
        H -= 1
    elif H < 0:
        H += 1
    R,G,B = colorsys.hsv_to_rgb(H,S,V)
    R *= 255
    G *= 255
    B *= 255
    newCode = RGBToHex(int(R),int(G),int(B))
    return newCode

"""
# Test Code

myHex = "ff6161"
R,G,B = hexToRGB(myHex)
print(f"#{myHex} gives R{R} G{G} B{B}")

identityHex = RGBToHex(R,G,B)
print(f"R{R} G{G} B{B} gives #{identityHex}")

transformedHex = hueShifter(myHex, 0.5)
print(f"#{myHex} shifts to #{transformedHex}")
"""

in_dir : str = "input/"
out_dir : str = "output/"
loopfor : int = len(sys.argv) - 1

if loopfor < 1:
    print("No command line arguments")
    exit

hueOffset : float = float(sys.argv[1])
if hueOffset < 0 or hueOffset > 1:
    print("The second argument must be a value between 0 and 1. That's the hue shift.")
    exit

i : int = 2
while i < loopfor + 1:
    inputPath = str(in_dir + sys.argv[i])
    outputPath = str(out_dir + sys.argv[i])

    if os.path.isfile(inputPath):
        with open(inputPath, "r") as input:
            document = input.read()
        with open(outputPath, "w") as output:
            startIndex = stopIndex = 0
            
            while stopIndex != -1:
                stopIndex = document.find('="#', startIndex)

                if stopIndex != -1:
                    oldColor = document[stopIndex + 3: stopIndex + 9]
                    #print(f"color {oldColor} index {stopIndex}")
                    newColor = hueShifter(oldColor, hueOffset)
                    output.write(str(document[startIndex:stopIndex] + '="#' + newColor))
                    startIndex = stopIndex + 9
                else:
                    output.write(str(document[startIndex:]))

    else:
        print(f"Could not find \"{sys.argv[i]}\" in \"{in_dir}\"")
    i += 1
