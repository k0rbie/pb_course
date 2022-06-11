from Graph import LockableGraph
from Constants import *


class Solver:
    def __init__(self, field):
        self.__field = field
        self.__graph = LockableGraph(FIELD_SIZE)
        self.__seq = []

    def solve(self):
        for i in range(FIELD_SIDE - 3):
            self.__fill_line(i, vertical=False)
            self.__fill_line(i, vertical=True)
        self.__fill_line(FIELD_SIDE - 3, vertical=False)
        self.__fill_two_of_five()
        self.__fill_last_three()
        return self.__seq

    def __in_place(self, *arr_ind):
        for ind in arr_ind:
            if self.__field.arr[ind] != ind + 1:
                return False
        return True

    def __add_moves(self, *moves):
        for move in moves:
            self.__seq.append(move)
            self.__field.space_swap(move)

    def __move_space_to(self, dest):
        prev = self.__field.space_ind
        path = self.__graph.shortest_path_search(prev, dest)  # n^2
        for i in path:
            self.__add_moves(i - prev)
            prev = i

    def __move_value_to(self, val, dest):
        prev = self.__field.value_ind(val)
        path = self.__graph.shortest_path_search(prev, dest)
        for i in path:  # n^3
            self.__graph.close_vert(prev)
            self.__move_space_to(i)           # n^2
            self.__graph.open_vert(prev)
            self.__add_moves(prev - i)
            prev = i

    def __fill_line(self, num, vertical):
        if vertical:
            along, across = DOWN, RIGHT  # fill column
            beg, end = (num + 1) * FIELD_SIDE + num, FIELD_SIDE*(FIELD_SIDE-1) + num
        else:
            along, across = RIGHT, DOWN  # fill row
            beg, end = num * (FIELD_SIDE + 1), FIELD_SIDE*(num + 1)-1
        if self.__in_place(*(range(beg, end + 1, along))):
            self.__graph.close_vert(*(range(beg, end + 1, along)))
            return
        for i in range(beg, end, along):
            self.__move_value_to(i + 1, i)
            self.__graph.close_vert(i)
        self.__move_space_to(end + across)
        if not self.__in_place(end):
            self.__move_value_to(end + 1, end + across)
            self.__graph.close_vert(end + across)
            self.__move_space_to(end + 2 * -along + across)
            path = [-across, along, along, across, -along, -across, -along, across]
            self.__add_moves(*path)
            self.__graph.open_vert(end + across)
            self.__graph.close_vert(end)

    def __fill_two_of_five(self):
        start = FIELD_SIZE + UP + 3 * LEFT
        if not self.__in_place(start, start + DOWN):
            self.__move_value_to(start + DOWN + 1, start)
            self.__graph.close_vert(start)
            self.__move_space_to(start + DOWN + RIGHT)
            if self.__field.arr[start + DOWN] == start + 1:
                path = [LEFT, UP, RIGHT, DOWN, RIGHT, UP, LEFT, LEFT, DOWN, RIGHT]
                self.__add_moves(*path)
            self.__move_value_to(start + 1, start + RIGHT)
            self.__graph.close_vert(start + RIGHT)
            self.__graph.open_vert(start)
            self.__move_value_to(start + DOWN + 1, start + DOWN)
            self.__graph.close_vert(start + DOWN)
            self.__add_moves(RIGHT)
            self.__graph.open_vert(start + RIGHT)
            self.__graph.close_vert(start)
        else:
            self.__graph.close_vert(start)
            self.__graph.close_vert(start + DOWN)

    def __fill_last_three(self):
        for ind in FIELD_SIZE + UP + LEFT - 1, FIELD_SIZE + UP - 1, FIELD_SIZE + LEFT - 1:
            self.__move_value_to(ind + 1, ind)
            self.__graph.close_vert(ind)
