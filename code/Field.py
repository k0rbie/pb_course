import math
import random
import sys
from random import shuffle
from solvability import *


def sign(value):
    if not value:
        return 0
    return math.copysign(1, value)


class Field:
    def __init__(self, side):
        self.side = side
        self.size = side * side
        self.arr = []
        self.fixed = [False] * 16
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

    def print(self):
        for i in range(self.side):
            for j in range(self.side):
                print(f"{self.arr[(i << 2) + j]: 3}".replace("16", "  "), end="")
            print()
        print()

    def ind(self, val):
        return self.arr.index(val)

    def invar(self) -> bool:
        inversions_par = num_inver(self.arr.copy()) % 2
        taxicab_par = self.ind(self.size) % 2
        return taxicab_par == inversions_par

    def space_swap(self, change):
        if self.move_validation(self.space+change):
            self.arr[self.space+change], self.arr[self.space] = \
                self.arr[self.space], self.arr[self.space+change]
            self.space += change
            self.update_space_coords()
            self.print()
            # time.sleep(0.5)
            return change
        else:
            print("Помилка: Спроба вийти за край поля!")
            sys.exit()

    def get_coords(self, ind):
        return ind % self.side, ind // self.side

    def move_validation(self, dest, start=None):
        if start is None:
            start = self.space
        return sum(self.count_dist(dest, start)) == 1 and not self.fixed[dest]

    def count_dist(self, ind_1, ind_2=None):
        if ind_2 is None:
            pos_2 = self.space_x, self.space_y
        else:
            pos_2 = self.get_coords(ind_2)
        pos_1 = self.get_coords(ind_1)
        return abs(pos_1[0] - pos_2[0]), abs(pos_1[1] - pos_2[1])

    def best_valid_moves(self, dest, start=None):
        if start is None:
            start = self.space
        best_moves = {}
        for i in (-1, 1, -4, 4):
            if start + i == dest:
                return [i]
            if self.move_validation((start + i) % self.size, start):
                dist = sum(self.count_dist(dest, start + i))
                if dist in best_moves:
                    best_moves[dist] += [i]
                else:
                    best_moves[dist] = [i]
        return best_moves[min(best_moves)]

    def move_space_to(self, dest: int):
        if self.fixed[dest]:
            print(f"fixed: {dest}")
            sys.exit()
            return
        if dest == self.space:
            print(f"ok: {dest}")
            # sys.exit()
            return
        prev = 0
        while self.space != dest:
            valid_moves = {}
            for i in (-1, 1, -4, 4):
                if self.move_validation((self.space + i) % self.size) and i != -prev:
                    dist = sum(self.count_dist(dest, self.space + i))
                    if dist in valid_moves:
                        valid_moves[dist] += [i]
                    else:
                        valid_moves[dist] = [i]
            if not len(valid_moves):
                valid_moves[sum(self.count_dist(dest, self.space + i))] = [-prev]
                print(f"{valid_moves=}")
            mins = valid_moves[min(valid_moves)]
            curr = random.choice(mins)
            prev = self.space_swap(curr)

    def move_value(self, value, dest):
        dest -= 1
        curr_ind = self.ind(value)
        self.fixed[curr_ind] = False
        while curr_ind != dest:
            moves = self.best_valid_moves(dest, curr_ind)
            print(moves)
            move = min(moves, key=lambda x: self.count_dist(curr_ind+x))
            self.fixed[curr_ind] = True
            print(self.fixed)
            self.move_space_to(curr_ind+move)
            self.fixed[curr_ind] = False
            print(self.fixed)
            self.move_space_to(curr_ind)
            curr_ind += move
        self.fixed[curr_ind] = True
