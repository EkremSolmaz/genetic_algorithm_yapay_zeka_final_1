from random import random, randint


class DNA(object):
    def __init__(self):
        # self.desire_to_eat = random() * 5 - 2.5
        # self.desire_to_survive = random() * 5 - 2.5
        # 0 - self.desire_to_eat = 1
        # 1 - self.desire_to_die = -1.1
        # 2 - self.food_view_distance = 1000
        # 3 - self.obstacle_view_distance = 200
        # 4 - self.max_force = 0.5
        # 5 - self.max_velocity = 10

        # All of them in a list
        self.dna = []
        self.randomize()

    def randomize(self):
        self.dna.append(random() * 5 - 2.5)    # 0 desire_to_eat [-2.5, 2.5]
        self.dna.append(random() * 5 - 2.5)    # 1 desire_to_die [-2.5, 2.5]
        self.dna.append(randint(50, 1000))      # 2 food_view_distance [50, 1000]
        self.dna.append(randint(50, 1000))      # 3 obstacle_view_distance [50, 1000]
        self.dna.append(random() * 1)          # 4 max_force [0, 2]
        self.dna.append(random() * 20)         # 5 max_velocity [0, 20]

    def print(self):
        print("desire_to_eat {}".format(self.dna[0]))
        print("desire_to_die {}".format(self.dna[1]))
        print("food_view_distance {}".format(self.dna[2]))
        print("obstacle_view_distance {}".format(self.dna[3]))
        print("max_force {}".format(self.dna[4]))
        print("max_velocity {}".format(self.dna[5]))
