import os
import sys


class Slice:
    def __init__(self, corner1, corner2):
        self.corner1 = corner1
        self.corner2 = corner2

    def __repr__(self):
        return " ".join([str(self.corner1[0]), str(self.corner2[0]), str(self.corner1[1]), str(self.corner2[1])])


def get_answer(path):
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
