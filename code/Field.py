from Graph import Graph
from InversionCounter import InversionCounter as InvCount
from random import shuffle
from Constants import *


class Field:
    def __init__(self):
        self.arr = []
        self.adj_list = Graph.puzzle_adj_list()
        for i in range(1, FIELD_SIZE + 1):
            self.arr.append(i)
        # self.inv_counter = InversionCounter()
        self.space = FIELD_SIZE - 1
        self.space_x = FIELD_SIDE - 1
        self.space_y = FIELD_SIDE - 1

    def find_space(self):
        self.space = self.ind(FIELD_SIZE)
        self.update_space_coords()

    def update_space_coords(self):
        self.space_x, self.space_y = self.get_coords(self.space)

    @staticmethod
    def get_coords(ind):
        return ind % FIELD_SIDE, ind // FIELD_SIDE

    def ind(self, val):
        return self.arr.index(val)

    def invar(self) -> bool:
        check_arr = self.arr.copy()
        check_arr.remove(FIELD_SIZE)
        inversions_par = InvCount.num_inver(check_arr) % 2
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
