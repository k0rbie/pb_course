from InversionCounter import InversionCounter as InvCount
from random import shuffle
from Constants import *


class Field:
    def __init__(self):
        self.arr = []
        for i in range(1, FIELD_SIZE + 1):
            self.arr.append(i)
        self.space_ind = FIELD_SIZE - 1
        self.space_x = FIELD_SIDE - 1
        self.space_y = FIELD_SIDE - 1

    def find_space(self):
        self.space_ind = self.value_ind(FIELD_SIZE)
        self.__update_space_coords()

    def __update_space_coords(self):
        self.space_x, self.space_y = \
            self.space_ind % FIELD_SIDE, self.space_ind // FIELD_SIDE

    def value_ind(self, val):
        return self.arr.index(val)

    def invar(self):
        check_arr = self.arr.copy()
        check_arr.remove(FIELD_SIZE)
        inversions_par = InvCount.num_inver(check_arr) % 2
        space_y_par = (FIELD_SIDE - self.space_y - 1) % 2
        return space_y_par == inversions_par

    def space_swap(self, change):
        if change in DIRECTIONS:
            self.two_elements_swap(self.space_ind, self.space_ind + change)
            self.__update_space_coords()

    def two_elements_swap(self, ind1, ind2):
        self.arr[ind1], self.arr[ind2] = self.arr[ind2], self.arr[ind1]
        self.find_space()

    def next_to_space(self, ind):
        return self.space_ind - ind in DIRECTIONS

    def shuffle_arr(self):
        prev = self.arr.copy()
        while self.is_sorted() or self.arr == prev:
            shuffle(self.arr)
        self.find_space()

    def is_sorted(self):
        return self.arr == list(range(1, FIELD_SIZE + 1))

    def matrix_view(self):
        res = ""
        for i in range(FIELD_SIDE):
            for j in range(FIELD_SIDE):
                res += f"{str(self.arr[i * FIELD_SIDE + j]).replace(str(FIELD_SIZE), '  '):>2} "
            res += "\n"
        return res
