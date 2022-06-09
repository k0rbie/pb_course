class MyQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, x):
        self.queue.append(x)        # 1

    def dequeue(self):
        return self.queue.pop(0)    # n
