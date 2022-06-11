class MyQueue:
    def __init__(self):
        self.__queue = []

    def enqueue(self, el):
        self.__queue.append(el)        # 1

    def dequeue(self):
        return self.__queue.pop(0)    # n
