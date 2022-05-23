from Field import Field


def main():
    field = Field(side)
    field.gen_valid()
    field.fixed += [0, 5]
    while True:
        field.move_space_to(int(input()) - 1)


if __name__ == '__main__':
    side = 4
    main()
