import os
import sys
import numpy as np
from scipy import signal
import itertools


class Slice:
    def __init__(self, matrix, corner1):
        self.top_left = corner1
        self.bottom_right = (corner1[0] + matrix.shape[0] - 1,
                             corner1[1] + matrix.shape[1] - 1)

    def get_matrix(self, pizza):
        a = pizza[np.ix_(range(self.top_left[0], self.bottom_right[0] + 1),
                         range(self.top_left[1], self.bottom_right[1] + 1))]

        return a

    def overlap(self, other):
        return self.do_overlap(self, other) or self.do_overlap(other, self)

    def do_overlap(self, s1, s2):
        if s1.top_left[0] <= s2.top_left[0] <= s1.bottom_right[0] <= s2.bottom_right[0] \
                and s1.top_left[1] <= s2.top_left[1] <= s1.bottom_right[1] <= s2.bottom_right[1]:
            return True

        if s2.top_left[0] <= s1.top_left[0] <= s1.bottom_right[0] <= s2.bottom_right[0] \
                and s2.top_left[1] <= s1.top_left[1] <= s1.bottom_right[1] <= s2.bottom_right[1]:
            return True

        if s2.top_left[0] <= s1.top_left[0] <= s1.bottom_right[0] <= s2.bottom_right[0] \
                and s1.top_left[1] <= s2.top_left[1] <= s2.bottom_right[1] <= s1.bottom_right[1]:
            return True

        if s1.top_left[0] <= s2.top_left[0] <= s1.bottom_right[0] <= s2.bottom_right[0] \
                and s2.top_left[1] <= s1.top_left[1] <= s2.bottom_right[1] <= s1.bottom_right[1]:
            return True

        return False

    def equal(self, other):
        return self.top_left[0] == other.top_left[0] \
            and self.top_left[1] == other.top_left[1] \
            and self.bottom_right[0] == other.bottom_right[0] \
            and self.bottom_right[1] == other.bottom_right[1]

    def __repr__(self):
        return " ".join([str(self.top_left[0]), str(self.top_left[1]), str(self.bottom_right[0]), str(self.bottom_right[1])])


class Solver:
    def __init__(self, spec, pizza):
        spec = spec.split(" ")
        self.row = int(spec[0])
        self.column = int(spec[1])
        self.min_ingredient = int(spec[2])
        self.max_slice = int(spec[3])

        self.pizza = np.zeros((self.row, self.column))
        self.db = dict()
        self.db['T'] = 0
        self.db['M'] = 1

        for i in range(self.row):
            for j in range(self.column):
                self.pizza[i][j] = self.db[pizza[i][j]]

    def solve(self):
        slices = self.populates_slices()

        #print("generate all combinations...")
        all_combinaisons = []
        # print(len(slices))
        for i in range(1, 6):
            current = [list(x) for x in itertools.combinations(slices, i)]
            all_combinaisons.extend(current)
            #print(i, len(all_combinaisons))

        # print(len(all_combinaisons))
        #print("looking for overlapping...")
        all_cuttings = []
        for cutting in all_combinaisons:
            if self.possible_cutting(cutting):
                all_cuttings.append(cutting)
        #print("get answer...")

        return self.print_answer(self.get_answer(all_cuttings))

    def possible_cutting(self, cutting):
        for i in range(len(cutting)):
            for j in range(i + 1, len(cutting)):
                if cutting[i].overlap(cutting[j]):
                    return False
        return True

    def print_answer(self, selected):
        answer = str(len(selected)) + "\r"
        for slice1 in selected:
            answer += str(slice1) + "\r"
        return answer

    def get_answer(self, all_cuttings):
        values = [sum([self.evaluate(f.get_matrix(self.pizza)) for f in cutting])
                  for cutting in all_cuttings]
        index = values.index(max(values))
        return all_cuttings[index]

    def add_if_not_overlap(self, cutting, s):
        for slic in cutting:
            if slic.overlap(s):
                return
        cutting.append(s)

    def evaluate(self, matrix):
        if matrix.size == 0:
            return 0

        shape = matrix.shape
        size = shape[0] * shape[1]
        if size > self.max_slice:
            return 0

        unique = np.unique(matrix, return_counts=True)
        if min(unique[1]) < self.min_ingredient or len(unique[1]) != 2:
            return 0
        return size

    def populates_slices(self):
        shape = self.pizza.shape
        all_step = []

        #print("generate slices...")
        for i in range(max(shape) + 1):  # range(max(shape)):
            all_step.extend(self.populate_matrix(i))

        #print("looking for valuable slices...")
        valuable_slices = []

        for slice1 in all_step:
            already_in = False
            matrix = slice1.get_matrix(self.pizza)
            if self.evaluate(matrix) <= 0:
                continue
            for slice2 in valuable_slices:
                if slice1.equal(slice2):
                    already_in = True
                    break
            if not already_in:
                valuable_slices.append(slice1)
        return valuable_slices

    def populate_matrix(self, step):
        matrix = self.pizza
        shape = matrix.shape
        list_step = []

        for i in range(min(self.max_slice, shape[0])):
            for j in range(min(self.max_slice - i + 1, shape[1])):

                mat = matrix[np.ix_(range(step, i + 1), range(j + 1))]
                list_step.append(Slice(mat, (step, 0)))

                mat = matrix[np.ix_(range(i + 1), range(step, j + 1))]
                list_step.append(Slice(mat, (0, step)))

                mat = matrix[np.ix_(range(step, i + 1), range(step, j + 1))]
                list_step.append(Slice(mat, (step, step)))

        return list_step


if __name__ == '__main__':
    all_lines = open(sys.argv[-1], "r").readlines()
    # print("init...")
    solver = Solver(all_lines[0], all_lines[1:len(all_lines)])
    answer = solver.solve()
    print(answer)
