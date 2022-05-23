from Field import Field
import timeit


def main():
    field = Field(side)
    field.gen_valid()
    field.move_value(1, 1)
    field.move_value(2, 2)
    field.move_value(5, 5)
    field.move_value(4, 16)
    field.move_value(3, 12)
    field.move_value(3, 8)
    field.move_value(4, 12)
    field.move_value(3, 4)
    field.move_value(4, 8)
    field.move_value(3, 3)
    field.move_value(4, 4)
    field.move_value(13, 16)
    field.move_value(9, 15)
    field.move_value(9, 14)
    field.move_value(13, 15)
    field.move_value(9, 13)
    field.move_value(13, 14)
    field.move_value(9, 9)
    field.move_value(13, 13)
    field.move_value(6, 6)
    field.move_value(8, 16)

    # while True:
    #     inp = tuple(map(int, input().split()))
    #     field.move_value(inp[0], inp[1])
        # field.move_space_to(int(input())-1)

if __name__ == '__main__':
    side = 4
    print(timeit.timeit(main, number=1))
