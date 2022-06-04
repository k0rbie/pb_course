import time

from Field import Field
from Solver import Solver
import timeit


def main():
    field = Field(side)
    field.gen_valid()
    control = Solver(field)
    while True:
        control.move_space_to(int(input())-1)



# Solver(field)
        # print("Solved\n\n")
        # time.sleep(0.2)


    # while True:
    #     inp = tuple(map(int, input().split()))
    #     field.move_value(inp[0], inp[1])
    # field.move_space_to(int(input())-1)

if __name__ == '__main__':
    side = 4
    print(timeit.timeit(main, number=1))
