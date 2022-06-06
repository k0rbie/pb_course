import time
from random import choice
import sys
from Field import Field
from Graph import LockableGraph
from copy import deepcopy
from Constants import *


class Solver:
    def __init__(self, field: Field):
        self.field = deepcopy(field)
        self.graph = LockableGraph()
        self.seq = []

    def solve(self):
        self.fill_row(0, 3)
        self.fill_column(4, 12)
        self.fill_row(5, 7)
        self.fill_last_six()
        return self.seq

    def add_moves(self, *moves):
        for move in moves:
            self.seq.append(move)
            self.field.space_swap(move)

    def move_space_to(self, dest: int):
        prev = self.field.space
        path = self.graph.shortest_path_search(prev, dest)
        for i in path:
            self.add_moves(i - prev)
            prev = i

    def move_value_to(self, val: int, dest: int):
        prev = self.field.ind(val)
        path = self.graph.shortest_path_search(prev, dest)
        for i in path:
            self.graph.close_vert(prev)
            self.move_space_to(i)
            self.graph.open_vert(prev)
            self.add_moves(prev - i)
            prev = i

    def fill_row(self, beg, end):
        if self.field.arr[beg:end+1] == list(range(beg+1, end+2)):
            return
        for i in range(beg, end):
            self.move_value_to(i + 1, i)
            self.graph.close_vert(i)
        self.move_space_to(end + FIELD_SIDE)
        if self.field.arr[end] != end + 1:
            self.move_value_to(end + 1, end + FIELD_SIDE)
            self.graph.close_vert(end + FIELD_SIDE)
            self.move_space_to(end - 2 + FIELD_SIDE)
            path = [-4, +1, +1, +4, -1, - 4, - 1, +4]
            self.add_moves(*path)
            self.graph.open_vert(end + FIELD_SIDE)
            self.graph.close_vert(end)

    def fill_column(self, beg, end):
        if self.field.arr[beg:end+1: FIELD_SIDE] == list(range(beg+1, end+2, FIELD_SIDE)):
            return
        for i in range(beg, end, FIELD_SIDE):
            self.move_value_to(i + 1, i)
            self.graph.close_vert(i)
        self.move_space_to(end + 1)
        if self.field.arr[end] != end + 1:
            self.move_value_to(end + 1, end + 1)
            self.graph.close_vert(end + 1)
            self.move_space_to(end - 2 * FIELD_SIDE + 1)
            path = [-1, +4, +4, +1, -4, - 1, - 4, +1]
            self.add_moves(*path)
            self.graph.open_vert(end + 1)
            self.graph.close_vert(end)

    def fill_last_six(self):
        start = FIELD_SIZE - FIELD_SIDE - 3
        if self.field.arr[start] != start + 1 or self.field.arr[start + FIELD_SIDE] != start + FIELD_SIDE + 1:
            self.move_value_to(start + 1 + FIELD_SIDE, start)
            self.graph.close_vert(start)
            self.move_space_to(start + FIELD_SIDE + 1)
            if self.field.arr[start + FIELD_SIDE] == start + 1:
                path = [-1, -4, +1, +4, +1, -4, -1, -1, +4]
                self.add_moves(*path)
            self.move_value_to(start + 1, start + 1)
            self.graph.close_vert(start + 1)
            self.graph.open_vert(start)
            self.move_value_to(start+FIELD_SIDE+1, start+FIELD_SIDE)
            self.graph.close_vert(start + FIELD_SIDE)
            self.add_moves(+1)
            self.graph.open_vert(start+1)
            self.graph.close_vert(start)
        else:
            self.graph.close_vert(start)
            self.graph.close_vert(start + FIELD_SIDE)

        for i in start + 1, start + 2, start + FIELD_SIDE + 1:
            self.move_value_to(i + 1, i)
            self.graph.close_vert(i)
