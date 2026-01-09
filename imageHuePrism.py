"""
    imageHuePrism.py

    takes a presumably red image and outputs the following counterparts:
    red, orange, yellow, green, cyan, blue, purple, pink, grayscale
"""

# Modified from

# https://stackoverflow.com/questions/7274221/changing-image-hue-with-python-pil
# Posted by unutbu, modified by community. See post 'Timeline' for change history
# Retrieved 2025-12-15, License - CC BY-SA 3.0

from PIL import Image
from sys import argv
from os import path
from pathlib import Path
import numpy as np

def input_validation(input : str):
    input = input.capitalize()
    if input in ["1", "Y", "YES"]:
        return True
    return False

def rgb_to_hsv(rgb):
    # Translated from source of colorsys.rgb_to_hsv
    # r,g,b should be a numpy arrays with values between 0 and 255
    # rgb_to_hsv returns an array of floats between 0.0 and 1.0.
    rgb = rgb.astype('float')
    hsv = np.zeros_like(rgb)
    # in case an RGBA array was passed, just copy the A channel
    hsv[..., 3:] = rgb[..., 3:]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maxc = np.max(rgb[..., :3], axis=-1)
    minc = np.min(rgb[..., :3], axis=-1)
    hsv[..., 2] = maxc
    mask = maxc != minc
    hsv[mask, 1] = (maxc - minc)[mask] / maxc[mask]
    rc = np.zeros_like(r)
    gc = np.zeros_like(g)
    bc = np.zeros_like(b)
    rc[mask] = (maxc - r)[mask] / (maxc - minc)[mask]
    gc[mask] = (maxc - g)[mask] / (maxc - minc)[mask]
    bc[mask] = (maxc - b)[mask] / (maxc - minc)[mask]
    hsv[..., 0] = np.select(
        [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default=4.0 + gc - rc)
    hsv[..., 0] = (hsv[..., 0] / 6.0) % 1.0
    return hsv

def hsv_to_rgb(hsv):
    # Translated from source of colorsys.hsv_to_rgb
    # h,s should be a numpy arrays with values between 0.0 and 1.0
    # v should be a numpy array with values between 0.0 and 255.0
    # hsv_to_rgb returns an array of uints between 0 and 255.
    rgb = np.empty_like(hsv)
    rgb[..., 3:] = hsv[..., 3:]
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    i = (h * 6.0).astype('uint8')
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    conditions = [s == 0.0, i == 1, i == 2, i == 3, i == 4, i == 5]
    rgb[..., 0] = np.select(conditions, [v, q, p, p, t, v], default=v)
    rgb[..., 1] = np.select(conditions, [v, v, v, q, p, p], default=t)
    rgb[..., 2] = np.select(conditions, [v, p, t, v, v, q], default=p)
    return rgb.astype('uint8')

def shift_hue(arr, new_hue, shift):
    hsv=rgb_to_hsv(arr)
    if shift:
        hsv[...,0] += new_hue
    else:
        hsv[...,0] = new_hue
    rgb=hsv_to_rgb(hsv)
    return rgb

def huePrism(filename : str, in_dir : str, out_dir : str, shift : bool, split_by_directory : bool):

    img = Image.open(in_dir + filename).convert('RGBA')
    arr = np.array(img)
    name, extension = path.splitext(path.basename(filename))

    hues = {
        "red": 0,
        "orange": 0.08,
        "yellow": 0.17,
        "green": 0.35,
        "cyan": 0.50,
        "blue": 0.62,
        "purple": 0.75,
        "pink": 0.88,
    }

    for hue in hues:
        new_img = Image.fromarray(shift_hue(arr,hues[hue],shift), 'RGBA')
        if split_by_directory:
            Path(out_dir + hue).mkdir(parents=True, exist_ok=True)
            new_img.save(str(out_dir + hue + "/" + name + extension))
        else:
            new_img.save(str(out_dir + name + "_" + hue + extension))

    gray_img = Image.open(in_dir + filename).convert('LA')
    if split_by_directory:
        Path(out_dir + "gray").mkdir(parents=True, exist_ok=True)
        gray_img.save(str(out_dir + "gray/" + name + extension))
    else:
        gray_img.save(str(out_dir + name + "_gray"+ extension))

in_dir = "input/"
out_dir = "output/"
loopfor : int = len(argv) - 1

shift = input_validation(input("Do you want to shift hues instead of set hues? [y/n]: "))
split_by_directory = input_validation(input("Do you want to split output by directories instead of name? [y/n]: "))
#print(f"shift {shift} directory {split_by_directory}")

if loopfor < 1:
    for img in Path(in_dir).rglob("*.png"):
        img_str = str(img)
        
        #print(str(img)[len(in_dir):])
        my_img = img_str[len(in_dir):]
        endpoint = my_img.rfind("\\")
        #print(f"backslash\\ {img_str[endpoint]}")
        new_in_dir = in_dir + my_img[0:endpoint] + "/"
        new_out_dir = out_dir + my_img[0:endpoint] + "/"
        #print(f"my_img {my_img}, endpoint {endpoint}, new in {new_in_dir}, new out {new_out_dir}")
        huePrism(img.name, new_in_dir, new_out_dir, shift, split_by_directory)
else:
    if __name__=='__main__':
        i : int = 1
        while i < loopfor + 1:
            huePrism(argv[i], in_dir, out_dir, shift, split_by_directory)
            i += 1
