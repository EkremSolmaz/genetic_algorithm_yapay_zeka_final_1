from graphics import *
from robot import *
from food import *
from obstacle import *
from population import *

from random import randint
from time import sleep, time

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
    foods.append(Food([randint(border_size, win_size-border_size),
                       randint(border_size, win_size-border_size)], win, False))

# Obstacle
obstacle_number = 10
obstacles = []
for i in range(obstacle_number):
    obstacles.append(Obstacle([randint(border_size, win_size-border_size),
                               randint(border_size, win_size-border_size)], win, False))

# Surround playable area with obstacles
r = obstacles[0].gui_size
x = border_size
y = win_size - border_size
for i in range((y - x) // (3 * r)):
    obstacles.append(Obstacle([x + (3 * i + 2) * r, x - r], win, False))  # up
    obstacles.append(Obstacle([x + (3 * i + 2) * r, y + r], win, False))  # down
    obstacles.append(Obstacle([x - r, x + (3 * i + 2) * r], win, False))  # left
    obstacles.append(Obstacle([y + r, x + (3 * i + 2) * r], win, False))  # right


# Robot
robot_number = 30
robots = []
map_limits = [border_size, win_size-border_size]
# r = Robot([400, 400], foods, obstacles, win, map_limits)

# Population
population = Population(robots)

skip_gen = 50
best_ofs = []
avgs = []


def erase_old_gui():
    for robot in robots:
        robot.remove_gui()


def get_most_succesful():
    max_score = 0
    avg_score = 0
    for robot in robots:
        if robot.score > max_score:
            max_score = robot.score
            avg_score += robot.score

    return max_score, avg_score / len(robots)


alive_robots = 0
start_pos = [randint(border_size + 10, win_size - border_size - 10),
             randint(border_size + 10, win_size - border_size - 10)]
for i in range(robot_number):
    robots.append(Robot(start_pos, foods, obstacles, win, map_limits, False))
    alive_robots += 1

while population.generation_cnt < skip_gen:  # dont simulate first n generation
    start_time = time()
    while alive_robots > 0:
        # sleep((len(robots) / alive_robots) * 0.002)  # Slow sim if less robots on

        alive_robots = 0
        for i in range(robot_number):
            robots[i].play()
            if robots[i].isAlive:
                alive_robots += 1

        if len(foods) < food_number:
            foods.append(
                Food([randint(border_size, win_size - border_size),
                      randint(border_size, win_size - border_size)], win, False))

        # End of while alive_robots > 0

    # erase_old_gui()
    best_score, avg_score = get_most_succesful()
    best_ofs.append(best_score)
    avgs.append(avg_score)
    print("Best of Gen Score: {}".format(best_score))
    print("Avg Gen Score: {}".format(avg_score))
    print("--------------")
    # best_dna.print()
    # print("--------------")

    robots = population.create_new_gen(False)

    for i in range(robot_number):
        if robots[i].isAlive:
            alive_robots += 1

    end_time = time()
    elapsed_time = end_time - start_time
    print("Elapsed Time : {}".format(elapsed_time))
    print("----------------------------------------------------------------------")


for food in foods:
    food.gui.undraw()
    food.create_gui()

for obstacle in obstacles:
    obstacle.create_gui()

for robot in robots:
    robot.simulate = True


while True:
    start_time = time()
    while alive_robots > 0:
        sleep((len(robots) / alive_robots) * 0.002)  # Slow sim if less robots on

        alive_robots = 0
        for i in range(robot_number):
            robots[i].play()
            if robots[i].isAlive:
                alive_robots += 1

        if len(foods) < food_number:
            foods.append(
                Food([randint(border_size, win_size - border_size),
                      randint(border_size, win_size - border_size)], win, True))

        # End of while alive_robots > 0

    erase_old_gui()

    best_score, avg_score = get_most_succesful()
    best_ofs.append(best_score)
    avgs.append(avg_score)
    print("Best of Gen Score: {}".format(best_score))
    print("Avg Gen Score: {}".format(avg_score))
    print("--------------")
    # best_dna.print()
    # print("--------------")

    robots = population.create_new_gen(True)

    for i in range(robot_number):
        if robots[i].isAlive:
            alive_robots += 1

    end_time = time()
    elapsed_time = end_time - start_time
    print("Elapsed Time : {}".format(elapsed_time))
    print("----------------------------------------------------------------------")

# win.close()
