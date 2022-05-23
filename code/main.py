import random
from random import shuffle
from math import ceil
from solvability import *
from Field import Field, Cell


def main():
    vector = vector_gen()
    # vector = list(range(1, 17))
    # print(vector)
    matrix = matrix_gen(vector)
    matrix_out(matrix)
    if not invar(vector):
        space_pos = vector.index(cell_num)
        vector[space_pos], vector[(space_pos+2) % cell_num] = vector[space_pos], vector[(space_pos+2) % cell_num]
    # move_value_to(vector, 1, 3)
    move_space_to(vector, 3)
    move_space_to(vector, 9)


def vector_gen() -> list[int]:
    global cell_num
    vector = list(range(1, cell_num + 1))
    shuffle(vector)
    return vector


def matrix_gen(vect: list[int]) -> list[list[int]]:
    global side
    matrix = []
    for i in range(side):
        row = []
        for j in range(side):
            row.append(vect[i * 4 + j])
        matrix.append(row)
    return matrix


def matrix_out(matrix: list[list[int]]) -> None:
    for i in matrix:
        for j in i:
            if j == 16:
                j = " "
            print(f"{j:3}", end="")
        print()
    print()


def invar(vector: list[int]) -> bool:
    inversions_par = num_inver(vector.copy()) % 2
    space_pos = vector.index(cell_num) + 1
    taxicab_par = (space_pos % side + ceil(space_pos / side)) % 2
    return taxicab_par == inversions_par


def solve_game(vector: list[int]):
    pass


def single_move(vector: list[int], move_ind, space_ind=None):
    if space_ind is None:
        space_ind = vector.index(cell_num)
    if space_ind == move_ind:
        return
    if move_validation(move_ind, space_ind):
        vector[move_ind], vector[space_ind] = vector[space_ind], vector[move_ind]
    matrix = matrix_gen(vector)
    matrix_out(matrix)


def move_validation(ind1: int, ind2: int):
    mod1 = ind1 % side
    mod2 = ind2 % side
    rem1 = ind1 // side
    rem2 = ind2 // side
    if mod1 == mod2 and abs(rem1-rem2) == 1:
        return True     # horizontal swap
    if rem1 == rem2 and abs(mod1-mod2) == 1:
        return True     # vertical swap
    print(f"Переміщувати із ({rem1+1}, {mod1+1}) у ({rem2+1}, {mod2+1}) не дозволено")
    return False


def move_space_to(vector: list[int], dest: int, curr=-1):
    if curr == -1:
        curr = vector.index(cell_num)
    while curr != dest:
        curr_pos = update_pos(curr)
        dest_pos = update_pos(dest)
        change = 0
        if dest_pos[0] > curr_pos[0]:
            change += 1
        elif dest_pos[0] < curr_pos[0]:
            change -= 1
        single_move(vector, curr, curr + change)
        curr += change
        change = 0
        if dest_pos[1] > curr_pos[1]:
            change += side
        elif dest_pos[1] < curr_pos[1]:
            change -= side
        single_move(vector, curr, curr + change)
        curr += change
        update_pos(curr)


def update_pos(vect_ind: int):
    return vect_ind % side, vect_ind // side


def count_dist(ind_1, ind_2):
    pos_1 = update_pos(ind_1)
    pos_2 = update_pos(ind_2)
    res = 0
    coords = zip(pos_1, pos_2)
    for i in coords:
        res += abs(i[0] - i[1])
    return res


def move_value_to(vector: list[int], value: int, dest: int):
    curr_ind = vector.index(value)
    while curr_ind != dest:
        curr_pos = update_pos(curr_ind)
        dest_pos = update_pos(dest)
        if curr_pos[0] == dest_pos[0]:
            if dest_pos[1] > curr_pos[1]:
                move_space_to(vector, curr_ind + 4)
            else:
                move_space_to(vector, curr_ind - 4)
        elif curr_pos[1] == dest_pos[1]:
            if dest_pos[0] > curr_pos[0]:
                move_space_to(vector, curr_ind + 1)
            else:
                move_space_to(vector, curr_ind - 1)


if __name__ == '__main__':
    side = 4
    cell_num = side ** 2
    # main()
    field = Field(side)
    field.print()
