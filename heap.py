from abc import ABC
from heapq import *
from random import random

from absqueue import *
from event import Event


class HeapQueue(AbstractPriorityQueue):
    def __init__(self):
        super().__init__()
        self.h = list()
        self.di = dict()

    def add_item(self, key, value=None):
        if key in self.di:
            key += (0.004 * random() + 0.001)
            value.end = key
        heappush(self.h, key)
        self.di[key] = value

    def __contains__(self, item):
        if item in self.di:
            return True
        return False

    def peek(self):
        try:
            return self.h[0], self.di[self.h[0]]
        except IndexError:
            return None, None

    def poll(self):
        try:
            k = heappop(self.h)
            v = self.di[k]
            self.di.pop(k)
            return k, v
        except IndexError:
            return None, None

    def remove(self):
        pass

    def empty(self):
        return len(self.h) == 0

    def __len__(self):
        return len(self.h)

    def __iter__(self):
        return iter(self.h)
