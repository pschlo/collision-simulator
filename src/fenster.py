try:
    from graphics import *
except ImportError as e:
    print(repr(e))
    print("\nZum Beenden Taste drücken...")
    input()
    exit()


class Fenster(GraphWin):
    def __init__(self, x, y):
        GraphWin.__init__(self, "Simulation", x, y)
        width_wall = 15
        width_floor = 6
        shift_wall = 20
        shift_floor = 50
        h_wall = 100
        self.x = x
        self.y = y
        self.setBackground("black")
        self.setCoords(0, 0, x, y)
        self.start = (shift_wall+width_wall-20, shift_floor+width_floor)
        self.length = x - shift_wall - width_wall

        floor = Line(Point(shift_wall, shift_floor + width_floor / 2),
                     Point(x, shift_floor + width_floor / 2))
        floor.setFill("white")
        floor.setWidth(width_floor)
        floor.draw(self)

        wall = Line(Point(int(width_wall / 2) + shift_wall, shift_floor + width_floor),
                    Point(int(width_wall / 2) + shift_wall, shift_floor + width_floor + h_wall))
        wall.setFill("white")
        wall.setWidth(width_wall)
        wall.draw(self)
