"""
    SPRITE3CostumeExtractor.py

    Extracts the costumes from a sprite with their names intact
"""

from zipfile import ZipFile
from json import load
from sys import argv

def extract_costumes(sprite_zip : str, in_dir : str, out_dir : str):

    with ZipFile(in_dir + sprite_zip, 'r') as z:
        with z.open('sprite.json') as f:
            sprite_data = load(f)

        for costume in sprite_data.get("costumes", []):
            with z.open(costume["md5ext"]) as src, open(out_dir + costume["name"] + "." + costume["dataFormat"], "wb") as dst:
                dst.write(src.read())

loopfor : int = len(argv) - 1
if loopfor < 1:
    print("Enter filenames as additional command line arguments")
    exit

print(argv)

in_dir = "input/"
out_dir = "output/"

if __name__=='__main__':
    i : int = 1
    while i < loopfor + 1:
        extract_costumes(argv[i], in_dir, out_dir)
        i += 1
