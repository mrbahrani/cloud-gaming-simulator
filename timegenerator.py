from abc import ABC


class TimeGenerator(ABC):
    def get_next_time(self):
        raise NotImplementedError
