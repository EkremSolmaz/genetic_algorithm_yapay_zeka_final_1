import numpy as np

from graphics import *
from dna import *

class Robot(object):
    def __init__(self, start_pos, foods, obstacles, gui_win, map_limits):
        self.position = start_pos  # position to create robot, [x, y]
        self.foods = foods  # list of foods to collect [obj, ..., obj]
        self.obstacles = obstacles  # list of obstacles to avoid [obj, ..., obj]
        self.map_limits = map_limits

        self.gui_win = gui_win  # window to draw objects
        self.gui_color = color_rgb(57, 76, 189)
        self.gui_dead_color = color_rgb(105, 95, 94)
        self.gui_h = 40
        self.gui_w = 20

        self.velocity = [0, 0]
        self.max_velocity = 15

        self.acceleration = [0, 0]

        self.direction = [0, -1]  # Always unit vector

        self.eat_distance = 10
        self.die_distance = 20

        self.isAlive = True

        self.dna = DNA()
        print(self.dna.desire_to_eat)
        print(self.dna.desire_to_die)

        self.create_gui()

    def create_gui(self):
        x, y = self.position[0], self.position[1]
        a, b = self.direction[0], self.direction[1]
        h, w = self.gui_h, self.gui_w

        vertices = [Point(x + a * h/2, y + b * h/2),
                    Point(x - a * h/2 + b * w/2, y - b * h/2 - a * w/2),
                    Point(x - a * h/2 - b * w/2, y - b * h/2 + a * w/2)]

        self.gui = Polygon(vertices)
        if self.isAlive:
            self.gui.setFill(self.gui_color)
        else:
            self.gui.setFill(self.gui_dead_color)
        self.gui.draw(self.gui_win)

    def set_direction(self, new_direction):
        self.direction = new_direction
        self.update_gui()

    def update_gui(self):
        self.gui.undraw()
        self.create_gui()

    def update(self):
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        if self.velocity[0] > self.max_velocity:
            self.velocity[0] = self.max_velocity
        if self.velocity[1] > self.max_velocity:
            self.velocity[1] = self.max_velocity

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Limit pos in borders
        if self.position[0] < self.map_limits[0]:
            self.position[0] = self.map_limits[0]
        if self.position[1] < self.map_limits[0]:
            self.position[1] = self.map_limits[0]
        if self.position[0] > self.map_limits[1]:
            self.position[0] = self.map_limits[1]
        if self.position[1] > self.map_limits[1]:
            self.position[1] = self.map_limits[1]

        self.update_gui()

        self.acceleration = [0, 0]

    def apply_force(self, force):
        self.acceleration[0] += force[0]
        self.acceleration[1] += force[1]

    def get_distance(self, pos):
        return np.sqrt((pos[0] - self.position[0]) ** 2 + (pos[1] - self.position[1]) ** 2)

    def get_closest_food(self):
        distances = []

        for food in self.foods:
            distances.append(self.get_distance(food.position))

        min_dist = 3000
        min_idx = -1
        for i in range(len(distances)):
            if distances[i] < min_dist:
                min_dist = distances[i]
                min_idx = i

        if min_dist < self.eat_distance:
            self.eat_food(min_idx)
            return self.get_closest_food()

        return min_idx

    def eat_food(self, food_idx):
        self.foods[food_idx].eat()

        self.foods[food_idx] = self.foods[-1]
        del self.foods[-1]

    def get_closest_obstacle(self):
        distances = []

        for obstacle in self.obstacles:
            distances.append(self.get_distance(obstacle.position))

        min_dist = 3000
        min_idx = -1
        for i in range(len(distances)):
            if distances[i] < min_dist:
                min_dist = distances[i]
                min_idx = i

        if min_dist < self.die_distance:
            self.die()
            return -1

        return min_idx

    def die(self):
        self.isAlive = False

    def seek(self):
        if self.isAlive:
            # Go to food
            target = self.foods[self.get_closest_food()]
            food_direction_unit = self.to_unit_vector([target.position[0] - self.position[0],
                                                       target.position[1] - self.position[1]])
            food_direction = [food_direction_unit[0] * self.max_velocity,
                              food_direction_unit[1] * self.max_velocity]
            steer_to_eat = self.to_unit_vector([food_direction[0] - self.velocity[0],
                                                food_direction[1] - self.velocity[1]])

            # Avoid obstacles
            avoid = self.obstacles[self.get_closest_obstacle()]
            obstacle_direction_unit = self.to_unit_vector([avoid.position[0] - self.position[0],
                                                           avoid.position[1] - self.position[1]])
            obstacle_direction = [obstacle_direction_unit[0] * self.max_velocity,
                                  obstacle_direction_unit[1] * self.max_velocity]
            steer_to_live = self.to_unit_vector([obstacle_direction[0] - self.velocity[0],
                                                 obstacle_direction[1] - self.velocity[1]])

            # final_steer = [steer_to_eat[0] * self.dna.desire_to_eat + steer_to_live[0] * self.dna.desire_to_survive,
            #                steer_to_eat[1] * self.dna.desire_to_eat + steer_to_live[1] * self.dna.desire_to_survive]

            steer_to_eat = [steer_to_eat[0] * self.dna.desire_to_eat,
                            steer_to_eat[1] * self.dna.desire_to_eat]

            steer_to_live = [steer_to_live[0] * self.dna.desire_to_die,
                             steer_to_live[1] * self.dna.desire_to_die]

            self.apply_force(steer_to_eat)
            self.apply_force(steer_to_live)
            self.update()

            self.set_direction(self.to_unit_vector(self.velocity))

    @staticmethod
    def to_unit_vector(vector):
        if vector[0] == 0 and vector[1] == 0:
            return vector

        length = np.sqrt(vector[0] ** 2 + vector[1] ** 2)
        unit_vector = [vector[0] / length, vector[1] / length]

        return unit_vector





