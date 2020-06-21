from graphics import *


class Obstacle(object):
    def __init__(self, pos, gui_win):
        self.position = pos

        self.gui_win = gui_win
        self.gui_color = color_rgb(186, 17, 45)
        self.gui_size = 10

        self.create_gui()

    def create_gui(self):
        obs = Rectangle(Point(self.position[0] - self.gui_size, self.position[1] - self.gui_size),
                        Point(self.position[0] + self.gui_size, self.position[1] + self.gui_size))
        obs.setFill(self.gui_color)
        obs.draw(self.gui_win)


