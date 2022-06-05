import time
from random import choice
import sys
from Field import Field
from Graph import LockableGraph


class Solver:
    def __init__(self, field: Field):
        self.field = field
        self.graph = LockableGraph(self.field.side)

    def start(self):
        pass

    def move_space_to(self, dest: int):
        prev = self.field.space
        path = self.graph.shortest_path_search(prev, dest)
        for i in path:
            self.field.space_swap(i - prev)
            prev = i

    def move_value_to(self, val: int, dest: int):
        prev = self.field.ind(val)
        path = self.graph.shortest_path_search(prev, dest)
        for i in path:
            self.graph.close_vert(prev)
            self.move_space_to(i)
            self.graph.open_vert(prev)
            self.field.space_swap(prev - i)
            prev = i

    def fill_row(self, beg, end):
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
            for i in path:
                self.field.space_swap(i)
            self.graph.open_vert(end + side)
            self.graph.close_vert(end)

    def fill_column(self, beg, end):
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
            for i in path:
                self.field.space_swap(i)
            self.graph.open_vert(end + 1)
            self.graph.close_vert(end)

    def fill_last_six(self):
        start = self.field.size - self.field.side - 3
        side = self.field.side
        self.move_value_to(start + 1 + side, start)
        self.graph.close_vert(start)
        self.move_space_to(start + side + 1)
        if self.field.arr[start + side] == start + 1:
            path = [-1, -4, +1, +4, +1, -4, -1, -1, +4]
            for i in path:
                self.field.space_swap(i)
        self.move_value_to(start + 1, start + 1)
        self.graph.close_vert(start + 1)
        self.graph.open_vert(start)
        self.move_value_to(start+side+1, start+side)
        self.graph.close_vert(start + side)
        self.field.space_swap(+1)
        self.graph.open_vert(start+1)
        self.graph.close_vert(start)

        for i in start + 1, start + 2, start + side + 1:
            self.move_value_to(i + 1, i)
            self.graph.close_vert(i)
