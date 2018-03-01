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
        self.used_steps = 0
        self.rides = []

    def canAccept(self, ride, max_steps):
        steps = self.totalTimeToRide(ride)
        return self.used_steps + steps < max_steps

    def addRide(self, ride):
        self.rides.append(ride)
        self.position = ride.arrive
        self.used_steps += self.totalTimeToRide(ride)

    def totalTimeToRide(self, ride):
        return self.position.distance(ride.depart) + ride.time_to_ride()


class Ride:
    def __init__(self, id, depart, arrive, start, finish):
        self.id = id
        self.depart = depart
        self.arrive = arrive
        self.start = start
        self.finish = finish

    def time_to_ride(self):
        return self.depart.distance(self.arrive)


class Solver:
    def __init__(self, shape, nb_steps, vehicles, rides):
        self.shape = shape
        self.vehicles = vehicles
        self.nb_steps = nb_steps
        self.rides = rides

    def solve(self):
        for ride in self.rides:
            times_to_ride = []
            for v in self.vehicles:
                times_to_ride.append((v, v.totalTimeToRide(ride)))
            min(times_to_ride,  key=lambda t: t[1])[0].addRide(ride)
        return self.vehicles


def parser(filename):
    my_file = open(filename)
    lines = my_file.readlines()
    sim_info = lines[0].split()
    i = 1
    rides_nb = len(lines) - 1
    rides = [None] * rides_nb
    while i < rides_nb + 1:
        ride_info = map(int, lines[i].split())
        rides[i - 1] = Ride(i - 1, Coordinates(ride_info[0], ride_info[1]),
                            Coordinates(ride_info[2], ride_info[3]),
                            ride_info[4], ride_info[5])
        i += 1

    vehicles = []
    for i in range(0, int(sim_info[2])):
        vehicles.append(Vehicles())

    return Solver(Coordinates(sim_info[0], sim_info[1]),
                  sim_info[5], vehicles, rides)


def answer(vehicles):
    final_answer = ""
    for v in vehicles:
        final_answer += "\r" + str(len(v.rides))
        for r in v.rides:
            final_answer += " " + str(r.id)
    return final_answer


if __name__ == '__main__':
    solver = parser(sys.argv[1])
    print(answer(solver.solve()))
