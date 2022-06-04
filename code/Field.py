import math
import sys
from random import shuffle
from solvability import *
from Graph import LockableGraph


def sign(value):
    if not value:
        return 0
    return math.copysign(1, value)


class Field:
    def __init__(self, side):
        self.side = side
        self.size = side * side
        self.arr = []
        self.graph = LockableGraph(self.side)
        for i in range(1, self.size + 1):
            self.arr.append(i)
        self.space = self.size - 1
        self.space_x = self.side - 1
        self.space_y = self.side - 1

    def gen_valid(self):
        self.shuffle_arr()
        if self.invar():
            self.print()
        else:
            swap_ind = (self.space + 2) % 16
            self.arr[swap_ind], self.arr[self.space] = self.arr[self.space], self.arr[swap_ind]
            self.space = swap_ind
            self.update_space_coords()
            self.print()

    def shuffle_arr(self):
        shuffle(self.arr)
        self.find_space()

    def find_space(self):
        self.space = self.ind(self.size)
        self.update_space_coords()

    def update_space_coords(self):
        self.space_x, self.space_y = self.get_coords(self.space)

    def get_coords(self, ind):
        return ind % self.side, ind // self.side

    def print(self):
        for i in range(self.side):
            for j in range(self.side):
                print(f"{self.arr[(i << 2) + j]: 3}".replace(str(self.size), "  "), end="")
            print()
        print()

    def ind(self, val):
        return self.arr.index(val)

    def invar(self) -> bool:
        inversions_par = num_inver(self.arr.copy()) % 2
        taxicab_par = self.ind(self.size) % 2
        return taxicab_par == inversions_par

    def space_swap(self, change):
        if not change:
            return change
        if self.near_space(self.space+change):
            self.arr[self.space+change], self.arr[self.space] = \
                self.arr[self.space], self.arr[self.space+change]
            self.space += change
            self.update_space_coords()
            self.print()
            # time.sleep(0.5)
            return change
        print(f"Помилка: Спроба вийти за край поля! {self.space + change}")
        self.print()
        sys.exit()

    def near_space(self, ind_1):
        return ind_1 in self.graph.adj_list[self.space]



