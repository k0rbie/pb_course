from Graph import LockableGraph
from Constants import *


class Solver:
    def __init__(self, field):
        self.field = field
        self.graph = LockableGraph(FIELD_SIZE)
        self.seq = []

    def solve(self):
        for i in range(FIELD_SIDE - 3):
            self.fill_line(i, vertical=False)
            self.fill_line(i, vertical=True)
        self.fill_line(FIELD_SIDE-3, vertical=False)
        self.fill_two_of_five()
        self.fill_last_three()
        return self.seq

    def in_place(self, *arr_ind):
        for ind in arr_ind:
            if self.field.arr[ind] != ind + 1:
                return False
        return True

    def add_moves(self, *moves):
        for move in moves:
            self.seq.append(move)
            self.field.space_swap(move)

    def move_space_to(self, dest: int):
        prev = self.field.space_ind
        path = self.graph.shortest_path_search(prev, dest)  # n^2
        for i in path:
            self.add_moves(i - prev)
            prev = i

    def move_value_to(self, val, dest):
        prev = self.field.ind(val)
        path = self.graph.shortest_path_search(prev, dest)
        for i in path:  # n^3
            self.graph.close_vert(prev)
            self.move_space_to(i)           # n^2
            self.graph.open_vert(prev)
            self.add_moves(prev - i)
            prev = i

    def fill_line(self, num, vertical):
        if vertical:
            along, across = DOWN, RIGHT  # fill column
            beg, end = (num + 1) * FIELD_SIDE + num, FIELD_SIDE*(FIELD_SIDE-1) + num
        else:
            along, across = RIGHT, DOWN  # fill row
            beg, end = num * (FIELD_SIDE + 1), FIELD_SIDE*(num + 1)-1
        if self.in_place(*(range(beg, end+1, along))):
            self.graph.close_vert(*(range(beg, end+1, along)))
            return
        for i in range(beg, end, along):
            self.move_value_to(i + 1, i)
            self.graph.close_vert(i)
        self.move_space_to(end + across)
        if not self.in_place(end):
            self.move_value_to(end + 1, end + across)
            self.graph.close_vert(end + across)
            self.move_space_to(end + 2 * -along + across)
            path = [-across, along, along, across, -along, -across, -along, across]
            self.add_moves(*path)
            self.graph.open_vert(end + across)
            self.graph.close_vert(end)

    def fill_two_of_five(self):
        start = FIELD_SIZE + UP + 3 * LEFT
        if not self.in_place(start, start + DOWN):
            self.move_value_to(start + DOWN + 1, start)
            self.graph.close_vert(start)
            self.move_space_to(start + DOWN + RIGHT)
            if self.field.arr[start + DOWN] == start + 1:
                path = [LEFT, UP, RIGHT, DOWN, RIGHT, UP, LEFT, LEFT, DOWN, RIGHT]
                self.add_moves(*path)
            self.move_value_to(start + 1, start + RIGHT)
            self.graph.close_vert(start + RIGHT)
            self.graph.open_vert(start)
            self.move_value_to(start+DOWN+1, start+DOWN)
            self.graph.close_vert(start + DOWN)
            self.add_moves(RIGHT)
            self.graph.open_vert(start+RIGHT)
            self.graph.close_vert(start)
        else:
            self.graph.close_vert(start)
            self.graph.close_vert(start + DOWN)

    def fill_last_three(self):
        for ind in FIELD_SIZE + UP + LEFT - 1, FIELD_SIZE + UP - 1, FIELD_SIZE + LEFT - 1:
            self.move_value_to(ind + 1, ind)
            self.graph.close_vert(ind)
