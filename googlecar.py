import sys


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, c):
        return abs(c.x - self.x) + abs(c.y - self.y)


class Vehicles:
    def __init__(self):
        self.position = Coordinates(0, 0)
        self.rides = []

    def canAccept(self, ride):
        steps = Coordinates(0, 0).distance(self.rides[0].depart)
        steps += ride.depart.distance(ride.arrive)

        # for ride in rides[1:]:
        #    steps +=

    def addRide(self, ride):
        self.rides.append(ride)
        self.position = ride.arrive

    def totalTimeToRide(self, ride):
        return self.position.distance(ride.depart) + ride.depart.distance(ride.arrive)


class Ride:
    def __init__(self, id, depart, arrive, start, finish):
        self.id = id
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

    def solve(self):
        for ride in self.rides:
            times_to_ride = [(vehicule, vehicule.totalTimeToRide(ride))
                             for vehicule in self.vehicles]
            print(times_to_ride)
            min(times_to_ride)[0].addRide(ride)
        return self.vehicles


def parser(filename):
    my_file = open(filename)
    lines = my_file.readlines()
    sim_info = lines[0].split()
    i = 1
    rides_nb = len(lines) - 1
    rides = [None] * rides_nb
    while i < rides_nb + 1:
        ride_info = lines[i]
        rides[i - 1] = Ride(i - 1, Coordinates(ride_info[0], ride_info[1]),
                            Coordinates(ride_info[2], ride_info[3]),
                            ride_info[4], ride_info[5])
        i += 1

    return Solver(Coordinates(sim_info[0], sim_info[1]),
                  sim_info[5], [Vehicles] * int(sim_info[2]), rides)


def answer(vehicles):
    answer = ""
    for v in vehicles:
        answer += "\r" + len(v.rides)
        for r in v.rides:
            answer += " " + r.id
    return answer


if __name__ == '__main__':
    solver = parser(sys.argv[1])
