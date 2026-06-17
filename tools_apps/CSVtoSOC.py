"""
    CSVtoSOC.py

    Lazy Python Script creates an SOC out of two CSVs denoting name and color
    Make the headers and size for the two CSV documents the same
    argv1 is the name document
    argv2 is the hex code document
    argv3 is the export name
"""

import csv
from sys import argv

def CSVtoSOC(name_file: str, code_file: str, export_name: str, in_dir: str, out_dir: str):

    with open(in_dir + name_file, "r") as names:
        with open(in_dir + code_file, "r") as codes:

            # Horrible type conversion at work
            color_names = csv.DictReader(names)
            color_codes = csv.DictReader(codes)

            color_names_list = list(color_names)
            color_codes_list = list(color_codes)

            color_names_simple = []
            color_codes_simple = []

            for dicts in color_names_list:
                for key in dicts:
                    color_names_simple.append(dicts[key])

            for dicts in color_codes_list:
                for key in dicts:
                    color_codes_simple.append(dicts[key])

            with open(out_dir + export_name, "w") as output:

                output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                output.write('<ooo:color-table xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svg="http://www.w3.org/2000/svg" xmlns:ooo="http://openoffice.org/2004/office">\n')
                for i in range(0,len(color_names_simple)):
                    output.write(f'<draw:color draw:name="{color_names_simple[i]}" draw:color="{color_codes_simple[i]}"/>\n')
                output.write('</ooo:color-table>')

# importlib execution
def main(*args):

    in_dir: str = args[0]
    out_dir: str = args[1]
    #leng: int = len(args)
    name_file: str = input("Enter the CSV for names: ")
    code_file: str = input("Enter the CSV for hexcodes: ")
    export_name: str = input("Enter export name: ")

    CSVtoSOC(name_file, code_file, export_name, in_dir, out_dir)

# regular execution
if __name__ == "__main__":

    in_dir = "input/"
    out_dir = "output/"

    CSVtoSOC(argv[1], argv[2], argv[3], in_dir, out_dir)
