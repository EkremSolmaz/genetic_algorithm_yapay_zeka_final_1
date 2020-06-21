from graphics import *
from robot import *
from food import *
from obstacle import *

from random import randint

from time import sleep

win_size = 800
win = GraphWin(width=win_size, height=win_size)

border_size = 50

map_color = color_rgb(70, 179, 94)

# DRAW MAP
map_up_left = Point(border_size, border_size)
map_down_right = Point(win_size - border_size, win_size-border_size)

rect = Rectangle(map_up_left, map_down_right)
rect.setFill(map_color)
rect.setOutline('red')
rect.draw(win)

# Food
foods = []
for i in range(10):
    foods.append(Food([randint(border_size, win_size-border_size), randint(border_size, win_size-border_size)], win))

# Obstacle
obstacles = []
for i in range(10):
    obstacles.append(Obstacle([randint(border_size, win_size-border_size),
                               randint(border_size, win_size-border_size)],
                              win))

# Robot
map_limits = [border_size, win_size-border_size]
r = Robot([400, 400], foods, obstacles, win, map_limits)
while r.isAlive:
    sleep(0.03)
    r.seek()
    # keyName = win.getKey()
    # if keyName == "Return":
    #     win.close()
    # elif keyName == "a":
    #     r.set_direction([-0.6, 0.8])
    # elif keyName == "s":
    #     r.set_direction([-0.8, -0.6])
    # elif keyName == "d":
    #     r.set_direction([1, 0])

win.getMouse()
win.close()
