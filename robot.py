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

        self.acceleration = [0, 0]

        self.direction = [0, -1]  # Always unit vector

        self.eat_distance = 10
        self.die_distance = 20

        self.isAlive = True

        self.dna = DNA()
        self.dna.print()

        self.max_velocity = self.dna.dna[5]

        self.create_gui()

    def create_gui(self):
        x, y = self.position[0], self.position[1]
        a, b = self.direction[0], self.direction[1]
        h, w = self.gui_h, self.gui_w

        vertices = [Point(x + a * h / 2, y + b * h / 2),
                    Point(x - a * h / 2 + b * w / 2, y - b * h / 2 - a * w / 2),
                    Point(x - a * h / 2 - b * w / 2, y - b * h / 2 + a * w / 2)]

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

        self.velocity[0] = max(-self.max_velocity, min(self.velocity[0], self.max_velocity))
        self.velocity[1] = max(-self.max_velocity, min(self.velocity[1], self.max_velocity))

        # print(self.velocity)
        self.set_direction(self.to_unit_vector(self.velocity))

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Limit pos in borders
        self.position[0] = max(self.map_limits[0], min(self.position[0], self.map_limits[1]))
        self.position[1] = max(self.map_limits[0], min(self.position[1], self.map_limits[1]))

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
            if distances[i] < min_dist and distances[i] < self.dna.dna[2]:
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
            if distances[i] < min_dist and distances[i] < self.dna.dna[3]:
                min_dist = distances[i]
                min_idx = i

        if min_dist < self.die_distance:
            self.die()
            return -1

        return min_idx

    def die(self):
        self.isAlive = False

    def play(self):
        if self.isAlive:
            steer_eat = self.eat()
            steer_avoid = self.avoid()

            steer_eat = self.vector_mul(steer_eat, self.dna.dna[0])
            steer_avoid = self.vector_mul(steer_avoid, self.dna.dna[1])

            self.apply_force(steer_eat)
            self.apply_force(steer_avoid)
            self.update()

    def eat(self):
        food_idx = self.get_closest_food()
        if food_idx == -1:
            # No food left
            return [0, 0]

        food_pos = self.foods[food_idx].position
        return self.get_steer(food_pos)

    def avoid(self):
        obstacle_idx = self.get_closest_obstacle()
        if obstacle_idx == -1:
            return [0, 0]

        obstacle_pos = self.obstacles[obstacle_idx].position
        return self.get_steer(obstacle_pos)

    def get_steer(self, pos):
        vector_to_object = self.vector_sub(pos, self.position)

        steer = self.to_unit_vector(self.vector_sub(vector_to_object, self.velocity))
        steer = self.vector_mul(steer, self.dna.dna[4])

        return steer

    @staticmethod
    def to_unit_vector(vector):
        if vector[0] == 0 and vector[1] == 0:
            return vector

        length = np.sqrt(vector[0] ** 2 + vector[1] ** 2)
        unit_vector = [vector[0] / length, vector[1] / length]

        return unit_vector

    @staticmethod
    def vector_mul(vector, mag):
        return [vector[0] * mag, vector[1] * mag]

    @staticmethod
    def vector_sub(vector1, vector2):
        return [vector1[0] - vector2[0], vector1[1] - vector2[1]]
