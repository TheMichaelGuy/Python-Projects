"""
    XLSXtoTable.py

    Converts an XLSX sheet into a sprite3 that contains a series of insertion list statements,
    functioning as a table

    sys arguments:
    argv 1 to n = excel sheets to convert (leave blank to convert all xlsx files in input)
"""

import pandas as pd
import json, zipfile, glob, os, random
from sys import argv

""" GLOBALS """

encoded_costume: str = "bcf454acf82e4504149f7ffe07081dbc"

costume_asset: dict = {
    "name": "costume1",
    "bitmapResolution": 1,
    "dataFormat": "svg",
    "assetId": f"{encoded_costume}",
    "md5ext": f"{encoded_costume}.svg",
    "rotationCenterX": 48,
    "rotationCenterY": 50
}

# Nice empty sprite :)
empty_sprite: str = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="0" height="0" viewBox="0 0 0 0">
  <!-- Exported by Scratch - http://scratch.mit.edu/ -->
</svg>"""

id_alphabet: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" #"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%()*+,-./:;=?@[]^_`{|}~"

""" FUNCTIONS """

# Force yes or no answers
def input_validation(input : str):
    input = input.capitalize()
    if input in ["1", "Y", "YES"]:
        return True
    return False

# Generates an ID that will hopefully resemble the IDs Scratch generates
# This may not matter as Scratch resolves most things when a sprite is imported and tends to leave
# metadata untouched. Have fun changing this if it matters!
def create_scratch_id(length=3):
    return ''.join(random.choice(id_alphabet) for _ in range(length))
# Below are more function calls which may be changed in case metadata norms are enforced
def create_variable_metadata():
    # ^:s83do}Wz;Si6}Km+i}
    return create_scratch_id()

def create_broadcast_metadata():
    # k5b[nyTc?m%K{W7Uf2d{
    return create_scratch_id()

def create_list_metadata():
    # A*DjFh?-k3Hp+Mvi$M:=
    return create_scratch_id()#

# Creates a pair of blocks for the "item (lenght of list) of list" block combos
def build_iol_lol_combo(iol_parent: str, list_name: str, list_name_id: str):
    length_of_list_block_id: str = create_scratch_id()
    item_of_list_block_id: str = create_scratch_id()
    item_of_list_block: dict = {
        "opcode": "data_itemoflist",
        "next": None,
        "parent": iol_parent,
        "inputs": {
            "INDEX": [
                3,
                length_of_list_block_id,
                [
                    7,
                    "1"
                ]
            ]
        },
        "fields": {
            "LIST": [
                list_name,
                list_name_id
            ]
        },
        "shadow": False,
        "topLevel": False
    }
    length_of_list_block: dict = {
        "opcode": "data_lengthoflist",
        "next": None,
        "parent": item_of_list_block_id,
        "inputs": {},
        "fields": {
            "LIST": [
                list_name,
                list_name_id
            ]
        },
        "shadow": False,
        "topLevel": False
    }
    return length_of_list_block_id, item_of_list_block_id, length_of_list_block, item_of_list_block

# Creates the blocks necessary for a "item (lenght of list) of list == value" condition
def build_eq_iol_lol_combo(eq_parent: str, value: str, list_name: str, list_name_id: str):
    equal_block_id: str = create_scratch_id()

    length_of_list_block_id, item_of_list_block_id, length_of_list_block, item_of_list_block = build_iol_lol_combo(equal_block_id, list_name, list_name_id)

    equal_block: dict = {
        "opcode": "operator_equals",
        "next": None,
        "parent": eq_parent,
        "inputs": {
            "OPERAND1": [
                3,
                item_of_list_block_id,
                [
                    10,
                    ""
                ]
            ],
            "OPERAND2": [
                1,
                [
                    10,
                    value
                ]
            ]
        },
        "fields": {},
        "shadow": False,
        "topLevel": False
    }

    return equal_block_id, length_of_list_block_id, item_of_list_block_id, equal_block, length_of_list_block, item_of_list_block

# Gets the metadata of where a list of insertion statements begins
def get_start_of_insertions(i: int, insert_dimensions: list[tuple[int, int]]):
    start: int = 0
    for x in range(0, i):
        start += insert_dimensions[x][0] * insert_dimensions[x][1]
    return start

# Converts an excel sheet to a Scratch sprite
def xlsx_to_sprite(file: str, costume_asset: dict, sprite_name: str = "Sprite1", use_sheet_names: bool = False, broadcast_name: str = "Menu: Open", variable_name: str = "currentMenu", list_name: str = "MENU: Menu List (Queue)"):
    # Import sheet
    print("Importing Sheet")
    excel: dict[str,pd.DataFrame] = pd.read_excel(file, sheet_name=None, dtype=str, keep_default_na=False, na_filter=False)

    # IDs for input variables
    broadcast_id: str = create_broadcast_metadata()
    variable_id: str = create_variable_metadata()
    list_name_id: str = create_list_metadata()

    ## Block Construction
    print("Beginning Block Construction")

    # Create Hat
    print("Hat Block")
    hat_block_id: str = create_scratch_id()
    loop_block_id: str = create_scratch_id()

    hat_block: dict = {
        "opcode": "event_whenbroadcastreceived",
        "next": loop_block_id,
        "parent": None,
        "inputs": {},
        "fields": {
            "BROADCAST_OPTION": [
                broadcast_name,
                broadcast_id
            ]
        },
        "shadow": False,
        "topLevel": True,
        "x": 100,
        "y": 100
    }
    # Loop
    wait_block_id: str = create_scratch_id()

    print("Loop Block")
    loop_block: dict = {
        "opcode": "control_forever",
        "next": None,
        "parent": hat_block_id,
        "inputs": {
            "SUBSTACK": [
                2,
                wait_block_id
            ]
        },
        "fields": {},
        "shadow": False,
        "topLevel": False
        }
    
    # Wait for menu change
    set_block_id: str = create_scratch_id()
    not_block_id: str = create_scratch_id()

    print("Initial Wait Condition")
    wait_block: dict = {
        "opcode": "control_wait_until",
        "next": set_block_id,
        "parent": loop_block_id,
        "inputs": {
            "CONDITION": [
                2,
                not_block_id
            ]
        },
        "fields": {},
        "shadow": False,
        "topLevel": False
    }

    equal_block_id: str = create_scratch_id()

    not_block: dict = {
        "opcode": "operator_not",
        "next": None,
        "parent": wait_block_id,
        "inputs": {
            "OPERAND": [
                2,
                equal_block_id
            ]
        },
        "fields": {},
        "shadow": False,
        "topLevel": False
    }
    iollol_eq = build_iol_lol_combo(equal_block_id, list_name, list_name_id)

    equal_block: dict = {
        "opcode": "operator_equals",
        "next": None,
        "parent": not_block_id,
        "inputs": {
            "OPERAND1": [
                3,
                [
                    12,
                    variable_name,
                    variable_id
                ],
                [
                    10,
                    ""
                ]
            ],
            "OPERAND2": [
                3,
                iollol_eq[1],
                [
                    10,
                    ""
                ]
            ]
        },
        "fields": {},
        "shadow": False,
        "topLevel": False
    }

    # Set new menu value
    print("Set Block")

    header_to_metadata: dict = {}
    index_to_header: list = []

    # Get metadata for all headers
    print("Creating Header Metadata")
    for sheet in excel:
        for col in excel[sheet].columns:
            if col not in header_to_metadata:
                header_to_metadata[col] = create_list_metadata()
                index_to_header.append(col)

    delete_statements_metadata: list[str] = [create_scratch_id() for _ in index_to_header]

    iollol_set = build_iol_lol_combo(set_block_id, list_name, list_name_id)
    set_block: dict = {
            "opcode": "data_setvariableto",
            "next": delete_statements_metadata[0], # first delete block
            "parent": wait_block_id,
            "inputs": {
                "VALUE": [
                    3,
                    iollol_set[1],
                    [
                        10,
                        "0"
                    ]
                ]
            },
            "fields": {
                "VARIABLE": [
                    variable_name,
                    variable_id
                ]
            },
            "shadow": False,
            "topLevel": False
    }

    # Reset all lists

    # Iterate Through Sheets
    print("Control Block Metadata")
    control_block_metadata: list[str] = [create_scratch_id() for sheet in excel]
    control_block_values: list[str] = []
    if use_sheet_names:
        control_block_values = [sheet for sheet in excel]
    else:
        control_block_values = [str(i) for i in range(0, len(excel))]

    # Delete all lists
    print("Creating Deletion Statements")
    delete_statements: list[dict] = []

    for i, col in enumerate(header_to_metadata):
        delete_statements.append(
            {
                "opcode": "data_deletealloflist",
                "next": (delete_statements_metadata[i + 1] if i != (len(index_to_header) - 1) else control_block_metadata[0]), # control if else
                "parent": (delete_statements_metadata[i - 1] if i != 0 else None), # set variable to
                "inputs": {},
                "fields": {
                    "LIST": [
                        col,
                        header_to_metadata[col]
                    ]
                },
                "shadow": False,
                "topLevel": False
            }
        )

    # Nested If Else Inserts

    control_blocks: list[dict] = []
    print("Condition Statements")
    control_conditions_data = [build_eq_iol_lol_combo(control_block_metadata[i], control_block_values[i], list_name, list_name_id) for i in range(0, len(control_block_metadata))]

    #eq_block_metadata: list[str] = [create_scratch_id() for sheet in excel]
    print("Insertion Metadata")
    insert_block_metadata: list[str] = []
    insert_dimensions: list[tuple[int,int]] = []
    a: int
    b: int
    for i, sheet in enumerate(excel):
        headers: list = excel[sheet].columns
        a = len(headers)
        for j, h in enumerate(headers): # h is the column, j enumerates it
            b = excel[sheet].shape[0] # it might make more sense to do excel[sheet].shape
            for k in range(0, excel[sheet].shape[0]): # k is the row
                insert_block_metadata.append(create_scratch_id())
        insert_dimensions.append((a,b))

    #print(f"Metadata Size: {len(insert_block_metadata)}")

    insert_blocks: list[dict] = []
    print("Begin Big Scary Loop")
    # NESTING
    for i, sheet in enumerate(excel):

        # Control Block
        insert_start = get_start_of_insertions(i, insert_dimensions)
        control_blocks.append(
            {
                "opcode": "control_if_else",
                "next": None,
                "parent": (control_block_metadata[i - 1] if i != 0 else delete_statements_metadata[-1]), # previous control or the last delete statement if first
                "inputs": {
                    "CONDITION": [
                        2,
                        control_conditions_data[i][0] #eq_block_metadata[i] # eqiollol
                    ],
                    "SUBSTACK": [
                        2,
                        insert_block_metadata[insert_start] # insert statements
                    ],
                    "SUBSTACK2": [
                        2,
                        (control_block_metadata[i + 1] if i != len(control_block_metadata) - 1 else None) # next control
                    ]
                },
                "fields": {},
                "shadow": False,
                "topLevel": False
            }
        )
        # Eq Iol Lol is already contructed

        # Insert Statements
        headers: list = excel[sheet].columns
        col_count: int = len(headers)
        row_count: int = excel[sheet].shape[0]
        #print(f"insert start: {insert_start} col: {col_count} row: {row_count} insert dim [0] {insert_dimensions[i][0]} [1] {insert_dimensions[i][1]}")
        for j, h in enumerate(headers): # h is the column, j enumerates it
            for k in range(0, row_count): # k is the row
                v = str(excel[sheet].iloc[k][h])
                # Rage-inducing index logic
                next_idx = (insert_start + row_count * j + k + 1 if k != (row_count - 1) else (insert_start + row_count * (j + 1) if j != (col_count - 1) else None))
                #current_idx = insert_start + (row_count * j) + k
                parent_idx = (insert_start + row_count * j + k - 1 if k != 0 else (insert_start + row_count * j - 1 if j != 0 else None))

                next = insert_block_metadata[next_idx] if next_idx is not None else None
                parent = insert_block_metadata[parent_idx] if parent_idx is not None else None
                
#                next = (insert_block_metadata[insert_start + insert_dimensions[i][0] * j + k + 1] if k != (row_count - 1) else (insert_block_metadata[insert_start + insert_dimensions[i][0] * (j + 1)] if j != (col_count - 1) else None)) # (insert_block_metadata[insert_start + insert_dimensions[i][0] * (j + 1)] if j != (col_count - 1) else None)
#                parent = (insert_block_metadata[insert_start + insert_dimensions[i][0] * j + k - 1] if k != 0 else (insert_block_metadata[insert_start + insert_dimensions[i][0] * j - 1] if j != 0 else control_block_metadata[i]))
                
                #print(f"parent: {parent_idx} current: {current_idx} next: {next_idx}")
                #print(f"\t\t\t\t\tv: {v} parent: {parent} current: {insert_block_metadata[insert_start + insert_dimensions[i][1] * j + k]} next: {next}")
                insert_blocks.append(
                    {
                        "opcode": "data_addtolist",
                        "next": next,  # null if last
                        "parent": parent, #control if else if 0
                        "inputs": {
                            "ITEM": [
                                1,
                                [
                                    10,
                                    v
                                ]
                            ]
                        },
                        "fields": {
                            "LIST": [
                                h, # column name and metadata
                                header_to_metadata[h]
                            ]
                        },
                        "shadow": False,
                        "topLevel": False
                    }
                )
            #print(h)
    #print(f"Headers {header_to_metadata}")

    # Put all blocks together
    # technically, the order of blocks don't matter since they have "next" and "parent" and their own identification

    # Initialize blocks
    print("Putting all blocks together")
    blocks: dict = {}

    # Hat, Loop, Wait
    blocks[hat_block_id] = hat_block
    blocks[loop_block_id] = loop_block
    blocks[wait_block_id] = wait_block
    blocks[not_block_id] = not_block
    blocks[iollol_eq[0]] = iollol_eq[2]
    blocks[iollol_eq[1]] = iollol_eq[3]
    blocks[equal_block_id] = equal_block
    # Set Block
    blocks[set_block_id] = set_block
    blocks[iollol_set[0]] = iollol_set[2]
    blocks[iollol_set[1]] = iollol_set[3]
    # Delete Lists
    for i in range(0, len(delete_statements_metadata)):
        blocks[delete_statements_metadata[i]] = delete_statements[i]
    # Control Blocks
    for i in range(0, len(control_block_metadata)):
        blocks[control_block_metadata[i]] = control_blocks[i]
    # Eq Iol Lol Combos
    for combo in control_conditions_data:
        blocks[combo[0]] = combo[3]
        blocks[combo[1]] = combo[4]
        blocks[combo[2]] = combo[5]
    # Insert Statements
    for i in range(0, len(insert_block_metadata)):
        blocks[insert_block_metadata[i]] = insert_blocks[i]

    # Build sprite.json
    sprite = {
            "isStage": False,
            "name": sprite_name,
            "variables": {},
            "lists": {}, # {lists[h][1]: [h, []] for h in headers} if make_local else {}
            "broadcasts": {},
            "blocks": blocks,
            "comments": {},
            "currentCostume": 0,
            "costumes": [costume_asset],
            "sounds": [],
            "volume": 100,
            "visible": True,
            "x": 0,
            "y": 0,
            "size": 100,
            "direction": 90,
            "draggable": False,
            "rotationStyle": "all around"
        }
    return sprite

def export_sprite(sprite : dict, sprite_name : str = "Sprite1"):
    with zipfile.ZipFile(sprite_name + ".sprite3", "w") as output:
        output.writestr("sprite.json", json.dumps(sprite))
        output.write(f"{encoded_costume}.svg", f"{encoded_costume}.svg")

def XLSXtoSPRITE3(file : str, in_dir : str, out_dir : str, costume_asset : dict, sprite_name : str = "Sprite1", use_sheet_names: bool = False, broadcast_name: str = "Menu: Open", variable_name: str = "currentMenu", list_name: str = "MENU: Menu List (Queue)"):
    sprite = xlsx_to_sprite(file=(in_dir + file), costume_asset=costume_asset, sprite_name=sprite_name, use_sheet_names=use_sheet_names, broadcast_name=broadcast_name, variable_name=variable_name, list_name=list_name)
    export_sprite(sprite=sprite, sprite_name=(out_dir + sprite_name))

""" CODE """

# importlib execution
def main(*args):

    in_dir: str = args[0]
    out_dir: str = args[1]
    leng: int = len(args)

    # Create Base Costume
    with open(f"{encoded_costume}.svg", "w") as costume:
        costume.write(empty_sprite)

    #make_local: bool = input_validation(input("Do you want the variables to be local to the sprite? [y/n]: "))
    use_sheet_names: bool = input_validation(input("Do you want to use sheet names as menu variables? Otherwise, the tables will increment starting at 1 [y/n]: "))
    broadcast_name: str = input("Enter a name for the broadcast that will activate the table: ")
    variable_name: str = input("Enter a name for the variable which will control the table: ")
    list_name: str = input("Enter a name for the list which will control the current table loaded: ")

    try:
        if leng < 3:
            for img in glob.glob(str(in_dir + '*.svg')):
                XLSXtoSPRITE3(img[len(in_dir):], in_dir, out_dir, costume_asset, os.path.splitext(img[len(in_dir):])[0], use_sheet_names, broadcast_name, variable_name, list_name)
        else:
            i: int = 2
            while i < leng:
                XLSXtoSPRITE3(args[i], in_dir, out_dir, costume_asset, os.path.splitext(args[i])[0], use_sheet_names, broadcast_name, variable_name, list_name)
                i += 1
    finally:
        # Delete Base Costume
        if os.path.isfile(f"{encoded_costume}.svg"):
            os.remove(f"{encoded_costume}.svg")    

# regular execution
if __name__ == "__main__":

    in_dir: str = "input/"
    out_dir: str = "output/"
    current_location : str = os.getcwd()

    argv.pop(0)
    argv.insert(0, current_location + "/" + in_dir)
    out_path : str = current_location + "/" + out_dir

    argv.insert(1, out_path)
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    main(*argv)