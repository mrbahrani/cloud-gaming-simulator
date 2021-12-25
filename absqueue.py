from abc import ABC


class AbstractPriorityQueue(ABC):
    def __init__(self):
        pass

    def add_item(self, key, value=None):
        raise NotImplementedError

    def __contains__(self, item):
        raise NotImplementedError

    def peek(self):
        raise NotImplementedError

    def poll(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

    def empty(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError
