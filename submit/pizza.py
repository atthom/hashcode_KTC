import os
import sys
import numpy as np
from scipy import signal
import itertools


class Slice:
    def __init__(self, matrix, corner1):
        self.matrix = matrix
        self.top_left = corner1
        self.bottom_right = (corner1[0] + matrix.shape[0] - 1,
                             corner1[1] + matrix.shape[1] - 1)

    def area(self):
        return (self.top_left[0] - self.top_left[1]) * (self.bottom_right[0] - self.bottom_right[1])

    def overlap(self, other):
        return self.do_overlap(self, other) or self.do_overlap(other, self)

    def do_overlap2(self, other):
        s_top_right = (self.top_left[0], self.bottom_right[1])
        s_bottom_left = (self.bottom_right[0], self.top_left[1])

        o_top_right = (other.top_left[0], other.bottom_right[1])
        o_bottom_left = (other.bottom_right[0], other.top_left[1])

        return not (s_top_right[0] > o_bottom_left[0]
                    or s_bottom_left[0] < o_top_right[0]
                    or s_top_right[1] > o_bottom_left[1]
                    or s_bottom_left[1] < o_top_right[1])

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

    def __repr__(self):
        return " ".join([str(self.top_left[0]), str(self.bottom_right[0]), str(self.top_left[1]), str(self.bottom_right[1])])


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

        a = slices[2]
        b = slices[21]
        c = slices[26]
        a2 = slices[0]
        # print(a.overlap(a2))

        # print(a.overlap(b))
       # print(a.overlap(c))
        # print(b.overlap(c))
        # print(b.overlap(a))
        # print(c.overlap(a))
        # print(c.overlap(b))
        good = [a, b, c]
        dd = [self.evaluate(f.matrix) for f in good]

        #all_permutations = list(itertools.permutations(slices))
        # print(len(all_permutations))
        all_cuttings = []

        for s in slices:
            current_cutting = [s]
            for other_slice in slices:
                self.add_if_not_overlap(current_cutting, other_slice)
            all_cuttings.append(current_cutting)

        return self.get_answer(all_cuttings)

    def get_answer(self, all_cuttings):
        values = [sum([self.evaluate(f.matrix) for f in cutting])
                  for cutting in all_cuttings]
        index = values.index(max(values))
        selected = all_cuttings[index]
        answer = str(len(selected)) + "\r"
        for slic in selected:
            answer += str(slic) + "\r"

        #answer += "\n"
        # for slic in selected:
        #    answer += str(slic.matrix) + "\n"
        return answer

    def add_if_not_overlap(self, cutting, s):
        for slic in cutting:
            if slic.overlap(s):
                return
        cutting.append(s)

    def no_one_overlap(self, cutting):
        for i in range(len(cutting)):
            for j in range(i + 1, len(cutting)):
                if cutting[i].overlap(cutting[j]):
                    return False
        return True

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
                    if np.array_equal(matmat[0], mat[0]) and matmat[1][0] == mat[1][0] and matmat[1][1] == mat[1][1]:
                        already_in = True
                        break
                if not already_in:
                    all_step_uniq.append(mat)

        valuable_slices = []
        for mat in all_step_uniq:
            if self.evaluate(mat[0]) > 0:
                valuable_slices.append(Slice(mat[0], mat[1]))

        return valuable_slices

    def populate_matrix(self, step):
        matrix = self.pizza
        shape = matrix.shape
        list_step = []

        for i in range(shape[0]):
            for j in range(shape[1]):
                mat = matrix[np.ix_(range(step, i + 1), range(j + 1))]
                list_step.append((mat, (step, 0)))

        for i in range(shape[0]):
            for j in range(shape[1]):
                mat = matrix[np.ix_(range(i + 1), range(step, j + 1))]
                list_step.append((mat, (0, step)))

        for i in range(shape[0]):
            for j in range(shape[1]):
                mat = matrix[np.ix_(range(step, i + 1), range(step, j + 1))]
                list_step.append((mat, (step, step)))

        return list_step


if __name__ == '__main__':
    all_lines = open(sys.argv[-1], "r").readlines()
    solver = Solver(all_lines[0], all_lines[1:len(all_lines)])
    answer = solver.solve()
    print(answer)
