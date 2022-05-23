import sys
from random import shuffle
from solvability import *


class Field:
    def __init__(self, side):
        self.side = side
        self.size = side * side
        self.arr = []
        for i in range(1, self.size + 1):
            self.arr.append(i)
        self.space = self.size - 1
        self.space_x = self.side - 1
        self.space_y = self.side - 1

    def gen_valid(self):
        self.shuffle_arr()
        if self.invar():
            self.print()
        else:
            swap_ind = (self.space + 2) % 16
            self.__swap(swap_ind - self.space)
            self.find_space()

    def shuffle_arr(self):
        shuffle(self.arr)
        self.find_space()

    def find_space(self):
        self.space = self.ind(self.size)
        self.space_x = self.space % 4
        self.space_y = self.space >> 2

    def print(self):
        for i in range(self.side):
            for j in range(self.side):
                print(f"{self.arr[(i << 2) + j]: 3}".replace("16", "  "), end="")
            print()
        print()

    def ind(self, val):
        return self.arr.index(val)

    def invar(self) -> bool:
        inversions_par = num_inver(self.arr.copy()) % 2
        taxicab_par = self.ind(self.size) % 2
        return taxicab_par == inversions_par

    def __swap(self, change):
        dest = self.space + change
        self.arr[dest], self.arr[self.space] = self.arr[self.space], self.arr[dest]
        self.space = dest
        self.print()

    def space_up(self):
        if self.space_y:
            self.__swap(-4)
            self.space_y -= 1
        else:
            print("Помилка: Пробіл на верхньому краю поля!")
            sys.exit()

    def space_down(self):
        if self.space_y != self.side - 1:
            self.__swap(+4)
            self.space_y += 1
        else:
            print("Помилка: Пробіл на нижньому краю поля!")
            sys.exit()

    def space_right(self):
        if self.space_x != self.side - 1:
            self.__swap(1)
            self.space_x += 1
        else:
            print("Помилка: Пробіл на правому краю поля!")
            sys.exit()

    def space_left(self):
        if self.space_x:
            self.__swap(-1)
            self.space_x -= 1
        else:
            print("Помилка: Пробіл на лівому краю поля!")
            sys.exit()

    def move_space_to(self, dest: int):
        while self.space != dest:
            dest_x = dest % 4
            dest_y = dest >> 2
            if dest_x > self.space_x:
                self.space_right()
            elif dest_x < self.space_x:
                self.space_left()
            if dest_y > self.space_y:
                self.space_down()
            elif dest_y < self.space_y:
                self.space_up()
