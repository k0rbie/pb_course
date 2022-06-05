class ConsoleInterface:
    def __init__(self, side, size, arr):
        self.side = side
        self.size = size
        self.arr = arr

    def show(self):
        for i in range(self.side):
            for j in range(self.side):
                print(f"{self.arr[(i << 2) + j]: 3}".replace(str(self.size), "  "), end="")
            print()
        print()
