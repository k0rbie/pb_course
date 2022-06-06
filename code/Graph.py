from MyQueue import MyQueue
from copy import deepcopy
from Constants import *


class Graph:
    def __init__(self, adj_list: dict[int: {int}]):
        self.adj_list = adj_list

    def shortest_path_search(self, beg: int, end):
        queue = MyQueue()
        p = [-1] * FIELD_SIZE
        p[beg] = None
        v = beg
        while v != end:
            for u in self.adj_list[v]:
                if p[u] == -1:
                    p[u] = v
                    queue.enqueue(u)
            # print(queue.queue)
            v = queue.dequeue()
        res = []
        while v != beg:
            res.append(v)
            v = p[v]
        return list(reversed(res))


class LockableGraph(Graph):
    def __init__(self):
        self.opened_vert = list(range(FIELD_SIZE))
        self.closed_vert = list()
        self.full = {i: [] for i in self.opened_vert}

        for i in range(FIELD_SIZE - FIELD_SIDE):
            self.full[i].append(i + FIELD_SIDE)
            self.full[i + FIELD_SIDE].append(i)

        ind = 0
        for i in range(FIELD_SIDE):
            for j in range(FIELD_SIDE - 1):
                self.full[ind].append(ind + 1)
                self.full[ind + 1].append(ind)
                ind += 1
            ind += 1

        Graph.__init__(self, deepcopy(self.full))

    def close_vert(self, *v):
        for i in v:
            if i in self.closed_vert:
                continue
            self.closed_vert.append(i)
            self.opened_vert.remove(i)
            for j in self.adj_list[i]:
                self.adj_list[j].remove(i)
            self.adj_list[i] = []

    def open_vert(self, *v):
        for i in v:
            if i in self.opened_vert:
                continue
            self.opened_vert.append(i)
            self.closed_vert.remove(i)
            for j in self.full[i]:
                if j not in self.closed_vert:
                    self.adj_list[j].append(i)
                    self.adj_list[i].append(j)
