from .level import *
from .cell import *
from .placeable import *

def code_to_level(code):
    code = code.split(";")
    width = int(code[1])
    height = int(code[2])
    level = Level(width, height)
    placeables = code[3].split(",")
    if(len(placeables) > 0):
        for pa in placeables:
            coords = pa.split(".")
            if(len(coords) > 1):
                level.add_placeable(placeable.Placeable(int(coords[0]), int(coords[1])))

    cells = code[4].split(",")
    if (len(cells) > 0):
        for cell in cells:
            values = cell.split(".")
            level.add_cell(Cell(int(values[3]), int(values[2]), int(values[0]), int(values[1])))

    level.add_description(code[5])

    return level

    print(code)