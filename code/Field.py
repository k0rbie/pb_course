from random import shuffle
from solvability import *


class Field:
    def __init__(self, side):
        self.side = side
        self.size = side * side
        self.arr = []
        for i in range(self.size):
            self.arr.append(Cell(i))
        self.space = self.arr[-1]
        self.space_ind = self.size - 1
        self.gen_valid()

    def gen_valid(self):
        self.shuffle_arr()
        if not self.invar():
            self.cell(self.size).single_move((self.arr[(self.space_ind + 2) % self.size]))

    def shuffle_arr(self):
        shuffle(self.arr)
        self.space = self.cell(self.size)
        self.space_ind = self.space.ind

    def print(self):
        for i in range(self.side):
            for j in range(self.side):
                print(f"{self.arr[(i << 2) + j].value: 3}".replace("16", "  "), end="")
            print()
        print()

    def index(self, val):
        return self.cell(val).ind

    def cell(self, val):
        for i in self.arr:
            if i.value == val:
                return i

    def update_space(self):
        self.space = self.cell(self.size)
        self.space_ind = self.space.ind

    def get_values(self):
        val_arr = []
        for i in self.arr:
            val_arr.append(i.value)
        return val_arr

    def invar(self) -> bool:
        inversions_par = num_inver(self.get_values()) % 2
        taxicab_par = self.index(self.size) % 2
        return taxicab_par == inversions_par


class Cell:
    def __init__(self, ind):
        self.value = ind + 1
        self.ind = ind
        self.x = ind // 4
        self.y = ind % 4
        self.fixed = False

    def single_move(self, cell):
        self.value, cell.value = cell.value, self.value

    def fix(self):
        self.fixed = True

    def unfix(self):
        self.fixed = False
