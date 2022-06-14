from InversionCounter import InversionCounter as InvCount
from random import shuffle
from Constants import *


class Field:
    def __init__(self):
        self.arr = []
        for i in range(1, FIELD_SIZE + 1):
            self.arr.append(i)
        self.space_ind = FIELD_SIZE - 1
        self.space_x = FIELD_SIDE - 1
        self.space_y = FIELD_SIDE - 1

    def find_space(self):     # оновлення параметрів індексів пробілу
        self.space_ind = self.value_ind(FIELD_SIZE)
        self.__update_space_coords()

    def __update_space_coords(self):    # оновлення параметрів стовпця та рядка пробілу
        self.space_x, self.space_y = \
            self.space_ind % FIELD_SIDE, self.space_ind // FIELD_SIDE

    def value_ind(self, val):   # повертає індекс певної клітинки
        return self.arr.index(val)

    def invar(self):    # перевіряє, чи може поле бути розвʼязаним
        check_arr = self.arr.copy()
        check_arr.remove(FIELD_SIZE)
        inv = InvCount(check_arr)
        inversions_par = inv.num_inver() % 2
        space_y_par = (FIELD_SIDE - self.space_y - 1) % 2
        return space_y_par == inversions_par

    def space_swap(self, change):   # змінює пробіл із сусідньою клітинкою
        if change in DIRECTIONS:
            self.two_elements_swap(self.space_ind, self.space_ind + change)
            self.__update_space_coords()

    def two_elements_swap(self, ind1, ind2):  # змінює місцями дві клітинки за індексами
        self.arr[ind1], self.arr[ind2] = self.arr[ind2], self.arr[ind1]
        self.find_space()

    def next_to_space(self, ind):   # перевіряє чи знаходиться клітинка поруч із пробілом
        return self.space_ind - ind in DIRECTIONS

    def shuffle_arr(self):  # змінює поле випадковим чином
        prev = self.arr.copy()
        while self.is_sorted() or self.arr == prev:
            shuffle(self.arr)
        self.find_space()

    def is_sorted(self):   # перевіряє чи відсортоване поле
        return self.arr == list(range(1, FIELD_SIZE + 1))

    def matrix_view(self):  # повертає рядок матричного представлення поля
        res = ""
        for i in range(FIELD_SIDE):
            for j in range(FIELD_SIDE):
                res += f"{str(self.arr[i * FIELD_SIDE + j]).replace(str(FIELD_SIZE), '  '):>2} "
            res += "\n"
        return res
