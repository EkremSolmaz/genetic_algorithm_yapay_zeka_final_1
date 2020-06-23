from robot import *
from food import *
from obstacle import *
from dna import *
from graphics import *
from random import random


class Population(object):
    def __init__(self, robots):
        self.robots = robots

        self.mutation_rate = 0.02

        self.generation_cnt = 0

    def create_new_gen(self):
        new_gen_robots = []

        fitness = dict()
        for i in range(len(self.robots)):
            fitness[i] = self.robots[i].score
            if fitness[i] < 0:
                fitness[i] = 0

        fitness = {k: v for k, v in sorted(fitness.items(), key=lambda item: item[1], reverse=True)}

        score_sum = 0
        for key in fitness:
            fitness[key] += score_sum
            score_sum = fitness[key]

        for i in range(len(self.robots)):
            mother_key = -1
            father_key = -1

            mother_rnd = random() * score_sum
            for x in fitness:
                if fitness[x] > mother_rnd:
                    mother_key = x
                    break

            father_rnd = random() * score_sum
            for x in fitness:
                if fitness[x] > father_rnd:
                    father_key = x
                    break

            new_robot = self.mate(self.robots[mother_key], self.robots[father_key])
            new_gen_robots.append(new_robot)

        self.generation_cnt += 1
        print("Generation {} has been created".format(self.generation_cnt))
        self.erase_old_gui()
        return new_gen_robots

    def mate(self, mother, father):
        child = Robot([400, 400],
                      self.robots[0].foods,
                      self.robots[0].obstacles,
                      self.robots[0].gui_win,
                      self.robots[0].map_limits)

        for i in range(len(child.dna.dna)):
            child.dna.dna[i] = (mother.dna.dna[i] + father.dna.dna[i]) / 2
            if random() < self.mutation_rate:
                a = child.dna.gen_ranges[i][0]
                b = child.dna.gen_ranges[i][1]
                mutation = (random() * (b-a) + a) * 0.1

                child.dna.dna[i] += mutation
                child.dna.dna[i] = max(a, min(child.dna.dna[1], b))

        return child

    def erase_old_gui(self):
        for robot in self.robots:
            robot.remove_gui()
