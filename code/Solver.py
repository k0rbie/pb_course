import time
from random import choice
import sys
from Field import Field
from Graph import LockableGraph
from copy import deepcopy


class Solver:
    def __init__(self, field: Field):
        self.field = deepcopy(field)
        self.graph = LockableGraph(self.field.side)
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
        side = self.field.side
        for i in range(beg, end):
            self.move_value_to(i + 1, i)
            self.graph.close_vert(i)
        self.move_space_to(end + side)
        if self.field.arr[end] != end + 1:
            self.move_value_to(end + 1, end + side)
            self.graph.close_vert(end + side)
            self.move_space_to(end - 2 + side)
            path = [-4, +1, +1, +4, -1, - 4, - 1, +4]
            self.add_moves(*path)
            self.graph.open_vert(end + side)
            self.graph.close_vert(end)

    def fill_column(self, beg, end):
        if self.field.arr[beg:end+1: self.field.side] == list(range(beg+1, end+2, self.field.side)):
            return
        side = self.field.side
        for i in range(beg, end, side):
            self.move_value_to(i + 1, i)
            self.graph.close_vert(i)
        self.move_space_to(end + 1)
        if self.field.arr[end] != end + 1:
            self.move_value_to(end + 1, end + 1)
            self.graph.close_vert(end + 1)
            self.move_space_to(end - 2 * side + 1)
            path = [-1, +4, +4, +1, -4, - 1, - 4, +1]
            self.add_moves(*path)
            self.graph.open_vert(end + 1)
            self.graph.close_vert(end)

    def fill_last_six(self):
        start = self.field.size - self.field.side - 3
        side = self.field.side
        if self.field.arr[start] != start + 1 or self.field.arr[start + side] != start + side + 1:
            self.move_value_to(start + 1 + side, start)
            self.graph.close_vert(start)
            self.move_space_to(start + side + 1)
            if self.field.arr[start + side] == start + 1:
                path = [-1, -4, +1, +4, +1, -4, -1, -1, +4]
                self.add_moves(*path)
            self.move_value_to(start + 1, start + 1)
            self.graph.close_vert(start + 1)
            self.graph.open_vert(start)
            self.move_value_to(start+side+1, start+side)
            self.graph.close_vert(start + side)
            self.add_moves(+1)
            self.graph.open_vert(start+1)
            self.graph.close_vert(start)
        else:
            self.graph.close_vert(start)
            self.graph.close_vert(start + side)

        for i in start + 1, start + 2, start + side + 1:
            self.move_value_to(i + 1, i)
            self.graph.close_vert(i)
