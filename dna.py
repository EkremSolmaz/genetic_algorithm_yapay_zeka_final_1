from random import random


class DNA(object):
    def __init__(self):
        # self.desire_to_eat = random() * 5 - 2.5
        # self.desire_to_survive = random() * 5 - 2.5
        self.desire_to_eat = 2
        self.desire_to_die = -1.5
        self.speed_coefficient = 10
        self.force_coefficient = 1
        self.distance_coefficient = 1
