from abc import ABC


class Controller(ABC):
    def set_path(self, packet):
        raise NotImplementedError

    def preprocess(self):
        raise NotImplementedError

    def initialize(self, *args):
        pass
