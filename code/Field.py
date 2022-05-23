import math
import sys
import time
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
        self.fixed = []
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
            time.sleep(0.5)
            return change
        else:
            print("Помилка: Спроба вийти за край поля!")
            sys.exit()

    def get_coords(self, ind):
        return ind % self.side, ind // self.side

    def move_validation(self, dest):
        return sum(self.count_dist(dest)) == 1 and dest not in self.fixed

    def mins(self, arr):
        arr_min = arr[0]
        for i in arr[1:]:
            if i < arr_min:


    def move_space_to(self, dest: int):
        if dest in self.fixed:
            print("?")
            return
        prev = 0
        while self.space != dest:
            valid_moves = []
            for i in (-1, 1, -4, 4):
                if self.move_validation((self.space + i) % self.size) and i != -prev:
                    valid_moves.append(i)
            if not len(valid_moves):
                valid_moves.append(-prev)
                print(f"{valid_moves=}")
                
            # curr = min(valid_moves, key=lambda x: sum(self.count_dist(dest, self.space + x)))
            prev = self.space_swap(curr)

    def count_dist(self, ind_1, ind_2=None):
        if ind_2 is None:
            pos_2 = self.space_x, self.space_y
        else:
            pos_2 = self.get_coords(ind_2)
        pos_1 = self.get_coords(ind_1)
        return abs(pos_1[0] - pos_2[0]), abs(pos_1[1] - pos_2[1])

    # def move_val(self, value, dest):
    #     curr_ind = self.ind(value)
    #     if curr_ind == dest:
    #         return
    #     x_sign, y_sign = tuple(map(sign, self.count_dist(dest, curr_ind)))
    #     options = []
    #     if not x_sign:
    #         if curr_ind + y_sign * self.side in self.fixed:
    #             pass
    #         elif y_sign == -1:
    #             self.space_down()
    #         else:   # y_sign == 1
    #             self.space_up()
    #
    #     elif not y_sign:
    #         option = curr_ind + x_sign
    #         if option in self.fixed:
    #             pass
    #         else:
    #             self.move_space_to(option)
    #     else:
    #         if x_diff != 0:
    #             options.append(curr_ind + sign(x_diff))
    #         if y_diff != 0:
    #             options.append(curr_ind + sign(y_diff))
