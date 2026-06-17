"""
    SPRITE3CostumeExtractor.py

    Extracts the costumes from a sprite with their names intact
"""

from zipfile import ZipFile
from json import load
from sys import argv
import glob

def extract_costumes(sprite_zip : str, in_dir : str, out_dir : str, use_header : bool):

    with ZipFile(in_dir + sprite_zip, 'r') as z:
        with z.open('sprite.json') as f:
            sprite_data = load(f)
        if use_header:
            for i, costume in enumerate(sprite_data.get("costumes", [])):
                with z.open(costume["md5ext"]) as src, open(out_dir + str(i + 1) + "_" + costume["name"] + "." + costume["dataFormat"], "wb") as dst:
                    dst.write(src.read())
        else:
            for costume in sprite_data.get("costumes", []):
                with z.open(costume["md5ext"]) as src, open(out_dir + costume["name"] + "." + costume["dataFormat"], "wb") as dst:
                    dst.write(src.read())

def input_validation(input : str):
    input = input.capitalize()
    if input in ["1", "Y", "YES"]:
        return True
    return False

loopfor : int = len(argv) - 1
if loopfor < 1:
    print("Enter filenames as additional command line arguments")
    exit

#print(argv)


# importlib execution
def main(*args):

    in_dir: str = args[0]
    out_dir: str = args[1]
    leng: int = len(args)
    use_header: bool = input_validation(input("Do you want to add numbers to order the sprites? [y/n]:"))

    if leng < 3:
        for img in glob.glob(str(in_dir + '*.sprite3')):
            extract_costumes(img[len(in_dir):], in_dir, out_dir, use_header)
    else:
        i: int = 2
        while i < leng:
            extract_costumes(args[i], in_dir, out_dir, use_header)
            i += 1

# regular execution
if __name__=='__main__':

    in_dir = "input/"
    out_dir = "output/"
    use_header: bool = input_validation(input("Do you want to add numbers to order the sprites? [y/n]:"))

    if loopfor < 1:
        for img in glob.glob(str(in_dir + '*.sprite3')):
            extract_costumes(img[len(in_dir):], in_dir, out_dir, use_header)
    else:
        i : int = 1
        while i < loopfor + 1:
            extract_costumes(argv[i], in_dir, out_dir, use_header)
            i += 1
