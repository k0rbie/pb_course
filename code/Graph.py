from MyQueue import MyQueue
from copy import deepcopy
from Constants import *


class Graph:
    def __init__(self, adj_list):
        self._adj_list = adj_list

    @staticmethod
    def puzzle_adj_list():  # повертає список суміжності для гри у 15
        _adj_list = {i: [] for i in range(FIELD_SIZE)}

        for i in range(FIELD_SIZE - FIELD_SIDE):
            _adj_list[i].append(i + FIELD_SIDE)
            _adj_list[i + FIELD_SIDE].append(i)

        ind = 0
        for i in range(FIELD_SIDE):
            for j in range(FIELD_SIDE - 1):
                _adj_list[ind].append(ind + 1)
                _adj_list[ind + 1].append(ind)
                ind += 1
            ind += 1
        return _adj_list

    def shortest_path_search(self, beg, end):  # знаходить найкоротший шлях між вершинами
        queue = MyQueue()
        p = [-1] * FIELD_SIZE
        p[beg] = None
        v = beg
        while v != end:  # n
            for u in self._adj_list[v]:  # n0^2
                if p[u] == -1:
                    p[u] = v
                    queue.enqueue(u)
            v = queue.dequeue()
        res = []
        while v != beg:
            res.append(v)
            v = p[v]
        return list(reversed(res))


class LockableGraph(Graph):
    def __init__(self, size):
        self.__opened_vert = set(range(size))

        self.__full = self.puzzle_adj_list()

        Graph.__init__(self, deepcopy(self.__full))

    def close_vert(self, *v):  # видаляє вершину
        for i in v:
            if i not in self.__opened_vert:
                continue
            self.__opened_vert.remove(i)
            for j in self._adj_list[i]:  # c
                self._adj_list[j].remove(i)  # n
            self._adj_list[i] = []

    def open_vert(self, *v):  # повертає раніше видалену вершину
        for i in v:
            if i in self.__opened_vert:
                continue
            self.__opened_vert.add(i)
            for j in self.__full[i]:  # c
                if j in self.__opened_vert:
                    self._adj_list[j].append(i)  # c
                    self._adj_list[i].append(j)  # c
