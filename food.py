from graphics import *


class Food(object):
    def __init__(self, pos, gui_win, visualize):
        self.position = pos
        self.is_alive = True

        self.gui_win = gui_win
        self.gui_color = color_rgb(209, 206, 10)
        self.gui_radius = 7

        self.gui = Circle(Point(self.position[0], self.position[1]), 7)

        if visualize:
            self.create_gui()

    def create_gui(self):
        self.gui.setFill(self.gui_color)
        self.gui.draw(self.gui_win)

    def eat(self):
        self.is_alive = False
        self.gui.undraw()
