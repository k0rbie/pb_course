from Graph import Graph
from random import shuffle
from Constants import *


class Field:
    def __init__(self):
        self.arr = []
        self.adj_list = Graph.puzzle_adj_list()
        for i in range(1, FIELD_SIZE + 1):
            self.arr.append(i)
        self.space = FIELD_SIZE - 1
        self.space_x = FIELD_SIDE - 1
        self.space_y = FIELD_SIDE - 1

    def find_space(self):
        self.space = self.ind(FIELD_SIZE)
        self.update_space_coords()

    def update_space_coords(self):
        self.space_x, self.space_y = self.get_coords(self.space)

    def get_coords(self, ind):
        return ind % FIELD_SIDE, ind // FIELD_SIDE

    def ind(self, val):
        return self.arr.index(val)

    def invar(self) -> bool:
        check_arr = self.arr.copy()
        check_arr.remove(FIELD_SIZE)
        inversions_par = self.num_inver(check_arr) % 2
        space_y_par = (FIELD_SIDE - self.space_y - 1) % 2
        return space_y_par == inversions_par

    def space_swap(self, change):
        if not change:
            return change
        if self.next_to_space(self.space + change):
            self.two_elements_swap(self.space, self.space+change)
            self.update_space_coords()
            return change

    def two_elements_swap(self, ind1, ind2):
        self.arr[ind1], self.arr[ind2] = self.arr[ind2], self.arr[ind1]
        self.find_space()

    def shuffle_arr(self):
        shuffle(self.arr)
        self.find_space()

    def next_to_space(self, ind_1):
        return ind_1 in self.adj_list[self.space]

    def num_inver(self, arr):
        return self.inv_merge_sort(arr, 0, len(arr) - 1)

    def inv_merge_sort(self, arr, l, r):
        if l == r:
            return 0
        m = r + l >> 1
        sw1 = self.inv_merge_sort(arr, l, m)
        sw2 = self.inv_merge_sort(arr, m + 1, r)
        arr[l:r + 1], swap_count = self.merge(arr, l, m, r)
        return sw1 + sw2 + swap_count

    def merge(self, arr, l1, r1, r2):
        i1 = l1
        i2 = r1 + 1
        new_arr = []
        swap_count = 0
        while i1 <= r1 and i2 <= r2:
            if arr[i1] <= arr[i2]:
                new_arr.append(arr[i1])
                i1 += 1
            else:
                new_arr.append(arr[i2])
                i2 += 1
                swap_count += r1 - i1 + 1
        new_arr += arr[i1:r1 + 1] + arr[i2:r2 + 1]
        return new_arr, swap_count


