"""
    3DSBMPConverter.py

    A modified version of BMPtoJPG.py to convert the top screenshots of a 3DS and delete the bottom screen
    WARNING: This deletes from the input directory
"""

from PIL import Image # pip install Pillow
import glob
import os

# importlib execution
def main(*args):

    in_dir: str = args[0]
    out_dir: str = args[1]
    #leng: int = len(args)

    for bot in glob.glob(str(in_dir + '*bot.bmp')):
        if os.path.isfile(bot):
            os.remove(bot)
    for top in glob.glob(str(in_dir + '*top.bmp')):
        name = top[top.find(os.path.basename(top)):top.find(".bmp")]
        print(f"converted {name}")
        Image.open(top).save(os.path.join(out_dir, name + '.jpg'))

# regular execution
if __name__ == "__main__":
    in_dir = "input/"
    out_dir = 'output/'
    for bot in glob.glob(str(in_dir + '*bot.bmp')):
        if os.path.isfile(bot):
            os.remove(bot)
    for top in glob.glob(str(in_dir + '*top.bmp')):
        name = top[top.find(os.path.basename(top)):top.find(".bmp")]
        print(f"converted {name}")
        Image.open(top).save(os.path.join(out_dir, name + '.jpg'))
