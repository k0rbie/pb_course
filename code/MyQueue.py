class MyQueue:
    def __init__(self):
        self.__queue = []

    def enqueue(self, el):  # дадає елемент в кінець черги
        self.__queue.append(el)

    def dequeue(self):  # видаляє та повертає перший елемент черги
        return self.__queue.pop(0)
