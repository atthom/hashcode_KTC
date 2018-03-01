import sys


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


def parser(filename):
    my_file = open(filename)
    lines = my_file.readlines()
    sim_info = lines[0].split()
    i = 1
    rides_nb = len(lines) - 1
    rides = [None] * rides_nb
    while i < rides_nb + 1:
        ride_info = lines[i]
        rides[i-1] = Ride(Coordinates(ride_info[0], ride_info[1]), Coordinates(ride_info[2], ride_info[3]), ride_info[4], ride_info[5])
        i += 1

    Solver(Coordinates(sim_info[0], sim_info[1]), sim_info[5], [Vehicles]*int(sim_info[2]), rides)


def solver():
    pass


def answer():
    print("1 0\r2 2 1")


if __name__ == '__main__':
    # answer()
    parser(sys.argv[1])
