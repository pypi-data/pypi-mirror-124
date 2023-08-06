from . import base74
from . import placeable

class Level:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.placeables = []
        self.cells = []
        self.description = ""

    def add_cell(self, c):
        self.cells.append(c)

    def add_placeable(self, p):
        self.placeables.append(p)

    def remove_object(self, x, y):
        for c in self.cells:
            if(c.x == x and c.y == y):
                self.cells.remove(c)
        for p in self.placeables:
            if(p.x == x and p.y == y):
                self.cells.remove(p)

    def add_description(self, description):
        self.description = description

    def __repr__(self):
        #V3;3;4;{)0b;;;0
        string = "V1;"
        string += str(self.width)
        string += ";"
        string += str(self.height)
        string += ";"
        for p in self.placeables:
            string += f"{p.x}.{p.y},"
        if(string[-1] == ","): string = string[:-1]
        string += ";"
        for c in self.cells:
            string += f"{c.type}.{c.angle}.{c.x}.{c.y},"
        if(string[-1] == ","): string = string[:-1]
        string += f";{self.description};"

        return string