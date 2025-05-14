"""
    BMPtoJPG.py

    Converts all .bmp files in input to .jpg in output
"""

# https://stackoverflow.com/questions/61551509/how-to-convert-bmp-images-to-png-in-python
# https://pillow.readthedocs.io/en/latest/handbook/tutorial.html#using-the-image-class

from PIL import Image # pip install Pillow
import glob
import os

in_dir = "input/"
out_dir = 'output/'
for img in glob.glob(str(in_dir + '*.bmp')):
    name = img[img.find(os.path.basename(img)):img.find(".bmp")]
    print(f"converted {name}")
    Image.open(img).save(os.path.join(out_dir, name + '.jpg'))
