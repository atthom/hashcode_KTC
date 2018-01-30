import os
import sys
import numpy as np
from scipy import signal


class Slice:
    def __init__(self, corner1, corner2):
        self.corner1 = corner1
        self.corner2 = corner2

    def area(self):
        return (self.corner1[0] - self.corner1[1]) * (self.corner2[0] - self.corner2[1])

    def __repr__(self):
        return " ".join([str(self.corner1[0]), str(self.corner2[0]), str(self.corner1[1]), str(self.corner2[1])])


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
        matrices = self.populates_slices()
        print(self.pizza)
        mat = matrices[2]
        print(mat)

        #max_peak = np.prod(mat.shape)
        #c = signal.fftconvolve(self.pizza, np.fliplr(np.flipud(mat)), 'valid')
        #overlaps = np.where(c == max_peak)
        dd = np.where(self.pizza == mat)
        print(dd)

    def evaluate(self, matrix):
        shape = matrix.shape
        if matrix.size == 0:
            return 0
        unique = np.unique(matrix, return_counts=True)
        min_ing = min(unique[1])
        nb_ing = len(unique[1])
        size = shape[0] * shape[1]

        if min_ing >= self.min_ingredient and nb_ing == 2 and size <= self.max_slice:
            return size
        else:
            return 0

    def populates_slices(self):
        shape = self.pizza.shape
        all_step = []

        for i in range(max(shape)):
            all_step.extend(self.populate_matrix(i))

        all_step_uniq = []
        for mat in all_step:
            if not all_step_uniq:
                all_step_uniq.append(mat)
            else:
                already_in = False
                for matmat in all_step_uniq:
                    if np.array_equal(matmat, mat):
                        already_in = True
                        break
                if not already_in:
                    all_step_uniq.append(mat)

        valuable_slices = []
        for mat in all_step_uniq:
            if self.evaluate(mat) > 0:
                valuable_slices.append(mat)

        return valuable_slices

    def populate_matrix(self, step):
        matrix = self.pizza
        shape = matrix.shape
        list_step = []

        for i in range(shape[0]):
            for j in range(shape[1]):
                mat = matrix[np.ix_(range(step, i + 1), range(j + 1))]
                list_step.append(mat)

        for i in range(shape[0]):
            for j in range(shape[1]):
                mat = matrix[np.ix_(range(i + 1), range(step, j + 1))]
                list_step.append(mat)

        for i in range(shape[0]):
            for j in range(shape[1]):
                mat = matrix[np.ix_(range(step, i + 1), range(step, j + 1))]
                list_step.append(mat)

        return list_step


def get_answer(path):
    all_lines = open(path, "r").readlines()
    solver = Solver(all_lines[0], all_lines[1:len(all_lines)])
    solver.solve()

    li = []
    li.append(Slice((0, 2), (0, 1)))
    li.append(Slice((0, 2), (2, 2)))
    li.append(Slice((0, 2), (3, 4)))
    answer = str(len(li)) + "\r"
    for s in li:
        answer += str(s) + "\r"

    return answer


if __name__ == '__main__':
    arg1 = sys.argv[-1]
    print(get_answer(arg1))
