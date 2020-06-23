from graphics import *
from robot import *
from food import *
from obstacle import *
from population import *

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
food_number = 40
foods = []
for i in range(food_number):
    foods.append(Food([randint(border_size, win_size-border_size), randint(border_size, win_size-border_size)], win))

# Obstacle
obstacle_number = 20
obstacles = []
for i in range(obstacle_number):
    obstacles.append(Obstacle([randint(border_size, win_size-border_size),
                               randint(border_size, win_size-border_size)], win))

# Surround playable area with obstacles
r = obstacles[0].gui_size
x = border_size
y = win_size - border_size
for i in range((y - x) // (3 * r)):
    obstacles.append(Obstacle([x + (3 * i + 2) * r, x - r], win))  # up
    obstacles.append(Obstacle([x + (3 * i + 2) * r, y + r], win))  # down
    obstacles.append(Obstacle([x - r, x + (3 * i + 2) * r], win))  # left
    obstacles.append(Obstacle([y + r, x + (3 * i + 2) * r], win))  # right


# Robot
robot_number = 20
robots = []
map_limits = [border_size, win_size-border_size]
# r = Robot([400, 400], foods, obstacles, win, map_limits)

# Population
population = Population(robots)

alive_robots = 0
for i in range(robot_number):
    robots.append(Robot([400, 400], foods, obstacles, win, map_limits))
    alive_robots += 1

while True:
    while alive_robots > 0:
        sleep((len(robots) / alive_robots) * 0.002)  # Slow sim if less robots on

        alive_robots = 0
        for i in range(robot_number):
            robots[i].play()
            if robots[i].isAlive:
                alive_robots += 1

        if len(foods) < food_number:
            foods.append(
                Food([randint(border_size, win_size - border_size), randint(border_size, win_size - border_size)], win))

    robots = population.create_new_gen()
    for i in range(robot_number):
        if robots[i].isAlive:
            alive_robots += 1

    win.getMouse()

win.close()
