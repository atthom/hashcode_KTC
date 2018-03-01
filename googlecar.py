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

    def canAccept(ride):
        pass

    def addRide(self, ride):
        self.rides.append(ride)
        self.position = ride.arrive

    def totalTimeToRide(self, ride):
        return self.position.distance(ride.depart) + ride.depart.distance(ride.arrive)


class Ride:
    def __init__(self, depart, arrive, start, finish, id):
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


def parser():
    pass


def answer(vehicles):
    answer = ""
    for v in vehicles:
        answer += "\r" + len(v.rides)
        for r in v.rides:
            answer += " " + r.id
    return answer


if __name__ == '__main__':
    pass
