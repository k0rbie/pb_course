import time
from random import choice
import sys


class Solver:
    def __init__(self, field):
        self.field = field
        # self.start()

    def start(self):
        self.move_value(1)
        self.move_value(2)
        self.move_value(5)
        self.move_value(4, 16)
        self.move_value(3, 12)
        self.move_value(3, 8)
        self.move_value(4, 12)
        self.move_value(3, 4)
        self.move_value(4, 8)
        self.move_value(3)
        self.move_value(4)
        self.move_value(13, 16)
        self.move_value(9, 15)
        self.move_value(9, 14)
        self.move_value(13, 15)
        self.move_value(9, 13)
        self.move_value(13, 14)
        self.move_value(9)
        self.move_value(13)
        self.move_value(6)
        self.move_value(8, 16)

    def move_space_to(self, dest: int):
        if self.field.fixed[dest]:
            print(f"fixed: {dest}")
            sys.exit()
            # return
        if dest == self.field.space:
            print(f"already there: {dest}")
            # sys.exit()
            return
        prev: int = 0
        while self.field.space != dest:
            valid_moves = {}
            for i in (-1, 1, -4, 4):
                if self.field.move_validation((self.field.space + i) % self.field.size) and i != -prev:
                    dist = sum(self.field.count_dist(dest, self.field.space + i))
                    if dist in valid_moves:
                        valid_moves[dist] += [i]
                    else:
                        valid_moves[dist] = [i]
            if not len(valid_moves):
                valid_moves[sum(self.field.count_dist(dest, self.field.space + i))] = [-prev]
            mins = valid_moves[min(valid_moves)]
            curr = choice(mins)
            prev = self.field.space_swap(curr)

    def move_value(self, value, dest=None):
        if dest is None:
            dest = value
        dest -= 1
        print(f"{value=}, {dest+1=}")
        print(self.field.fixed)
        self.field.print()
        print("\n")
        value_ind = self.field.ind(value)
        self.field.fixed[value_ind] = False
        count = 0
        while value_ind != dest:
            if count == 30:
                print("Забагато кроків")
                sys.exit()
            moves = self.best_valid_moves(dest, value_ind)
            move = min(moves, key=lambda x: self.field.count_dist(value_ind+x))
            self.field.fixed[value_ind] = True
            # print(self.field.fixed)
            self.move_space_to(value_ind+move)
            self.field.fixed[value_ind] = False
            # print(self.field.fixed)
            self.move_space_to(value_ind)
            value_ind += move
        self.field.fixed[value_ind] = True


    def best_valid_moves(self, dest, start=None):
        if start is None:
            start = self.field.space
        best_moves = {}
        for i in (-1, 1, -4, 4):
            if start + i == dest:
                return [i]
            if self.field.move_validation((start + i) % self.field.size, start):
                dist = sum(self.field.count_dist(dest, start + i))
                if dist in best_moves:
                    best_moves[dist] += [i]
                else:
                    best_moves[dist] = [i]
        if not len(best_moves):
            print(f"Не знайдено доступних кроків {start=}, {dest=}")
            print(self.field.fixed)
            self.field.print()
        return best_moves[min(best_moves)]
