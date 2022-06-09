from MyQueue import MyQueue
from copy import deepcopy
from Constants import *


class Graph:
    def __init__(self, adj_list):
        self.adj_list = adj_list

    @staticmethod
    def puzzle_adj_list():  # n = n0 ^ 2
        adj_list = {i: [] for i in range(FIELD_SIZE)}

        for i in range(FIELD_SIZE - FIELD_SIDE):
            adj_list[i].append(i + FIELD_SIDE)
            adj_list[i + FIELD_SIDE].append(i)

        ind = 0
        for i in range(FIELD_SIDE):
            for j in range(FIELD_SIDE - 1):
                adj_list[ind].append(ind + 1)
                adj_list[ind + 1].append(ind)
                ind += 1
            ind += 1
        return adj_list

    def shortest_path_search(self, beg, end):
        queue = MyQueue()
        p = [-1] * FIELD_SIZE
        p[beg] = None
        v = beg
        while v != end:  # n
            for u in self.adj_list[v]:  # n0^2
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
        self.opened_vert = set(range(size))
        self.closed_vert = set()

        self.full = self.puzzle_adj_list()

        Graph.__init__(self, deepcopy(self.full))

    def close_vert(self, *v):
        for i in v:
            if i in self.closed_vert:
                continue
            self.closed_vert.add(i)
            self.opened_vert.remove(i)
            for j in self.adj_list[i]:  # c
                self.adj_list[j].remove(i)  # n
            self.adj_list[i] = []

    def open_vert(self, *v):
        for i in v:
            if i in self.opened_vert:
                continue
            self.opened_vert.add(i)
            self.closed_vert.remove(i)
            for j in self.full[i]:  # c
                if j not in self.closed_vert:
                    self.adj_list[j].append(i)  # c
                    self.adj_list[i].append(j)  # c
