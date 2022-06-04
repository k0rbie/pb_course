from Queue import Queue


class Graph:
    def __init__(self, adj_list: dict[int: {int}]):
        self.adj_list = adj_list
        self.size = len(adj_list)

    def shortest_path_search(self, beg: int, end):
        queue = Queue()
        queue.enqueue(beg)
        p = [None] * self.size
        v = beg
        while v != end:
            for u in self.adj_list[v]:
                if p[u] is not None:
                    p[u] = v
                    queue.enqueue(u)
            v = queue.dequeue()
        res = []
        while v is not None:
            res.append(v)
            v = p[v]
        return res

