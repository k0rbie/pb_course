from Queue import Queue


class Graph:
    def __init__(self, adj_list: dict[int: {int}]):
        self.adj_list = adj_list
        self.size = len(adj_list)


    def add_vert(self, v):
        pass

    def shortest_path_search(self, beg: int, end):
        queue = Queue()
        p = [-1] * self.size
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
        while v is not None:
            res.append(v)
            v = p[v]
        return list(reversed(res))


class LockableGraph(Graph):
    def __init__(self, side):
        size = side * side
        self.opened_vert = list(range(size))
        self.closed_vert = list()
        self.full = {i: [] for i in self.opened_vert}

        for i in range(size - side):
            self.full[i].append(i + side)
            self.full[i + side].append(i)

        ind = 0
        for i in range(side):
            for j in range(side - 1):
                self.full[ind].append(ind + 1)
                self.full[ind + 1].append(ind)
                ind += 1
            ind += 1

        print(self.full)
        Graph.__init__(self, self.full.copy())

    def close_vert(self, *v):
        for i in v:
            self.closed_vert.append(i)
            self.opened_vert.remove(i)
            for j in self.adj_list[i]:
                self.adj_list[j].remove(i)
                self.adj_list[i].remove(j)

    def open_vert(self, *v):
        for i in v:
            self.opened_vert.append(i)
            self.closed_vert.remove(i)
            for j in self.full[i]:
                if j not in self.closed_vert:
                    self.adj_list[j].append(i)
                    self.adj_list[i].append(j)


grid = LockableGraph(side=4)


grid.close_vert(0, 5, 9)
print(grid.shortest_path_search(1, 4))
