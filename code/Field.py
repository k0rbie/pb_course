import sys
import time

from solvability import *
from Graph import LockableGraph
from PyQt5.QtWidgets import QApplication
from Constants import *


class Field:
    def __init__(self):
        self.arr = []
        self.graph = LockableGraph()
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
        inversions_par = num_inver(check_arr) % 2
        space_y_par = (FIELD_SIDE - self.space_y - 1) % 2
        return space_y_par == inversions_par

    def space_swap(self, change):
        if not change:
            return change
        if self.near_space(self.space+change):
            self.two_elements_swap(self.space, self.space+change)
            self.update_space_coords()
            return change

    def two_elements_swap(self, ind1, ind2):
        self.arr[ind1], self.arr[ind2] = self.arr[ind2], self.arr[ind1]
        self.find_space()

    def near_space(self, ind_1):
        return ind_1 in self.graph.adj_list[self.space]
