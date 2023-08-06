class Cell:
    def __init__(self, x, y, type, angle):
        self.x = x
        self.y = y
        self.type = type
        self.angle = angle

class GeneratorCell(Cell):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 0, angle)

class CWRotatorCell(Cell):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 1, angle)

class CCWRotatorCell(Cell):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 2, angle)

class MoveCell(Cell):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 3, angle)

class SlideCell(Cell):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 4, angle)

class PushCell(Cell):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 5, angle)

class ImmobileCell(Cell):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 6, angle)

class EnemyCell(Cell):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 7, angle)

class TrashCell(Cell):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 8, angle)