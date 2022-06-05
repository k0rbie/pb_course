import sys
import time

from Field import Field
from Solver import Solver
from face import Ui_MainWindow
import timeit


def main():
    field = Field(side)
    for i in range(1):
        field.gen_valid()
        ctrl = Solver(field)
        ctrl.fill_row(0, 3)
        ctrl.fill_column(4, 12)
        ctrl.fill_row(5, 7)
        ctrl.fill_last_six()
        # field.print()
        print("clap")


def value(control):
    inp = tuple(map(int, input().split()))
    control.move_value_to(inp[0], inp[1])


def space(control):
    control.move_space_to(int(input()))




# Solver(field)
        # print("Solved\n\n")
        # time.sleep(0.2)



if __name__ == '__main__':
    side = 4
    print(timeit.timeit(main, number=1))
