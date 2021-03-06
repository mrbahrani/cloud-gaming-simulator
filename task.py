import math


class Task:
    def __init__(self, required_memory=0, required_mips=100, max_pes=math.inf, num_obj=3):
        self.required_memory = required_memory
        self.required_mips = required_mips
        self.maximum_pes = math.inf
        self.number_of_objects = num_obj
        self.completed = False
