from utils import *


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, c):
        pass


class Vehicles:
    def __init__(self):
        self.position = Coordinates(0, 0)

    def TotalTimeToRide(ride):
        pass


class Ride:
    def __init__(self, depart, arrive, start, finish):
        self.depart = depart
        self.arrive = arrive
        self.start = start
        self.finish = finish


class Solver:
    def __init__(self, shape, nb_steps, vehicles, rides):
        self.shape = shape
        self.vehicles = vehicles
        self.nb_steps = nb_steps
        self.rides = rides


def parser():
    pass


def solver():
    pass


def answer():
    print("1 0\r2 2 1")


if __name__ == '__main__':
    answer()
