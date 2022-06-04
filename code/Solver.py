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


