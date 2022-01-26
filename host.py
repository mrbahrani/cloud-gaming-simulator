import math
from queue import Queue
from random import random

from distributanmaker import DistributionMaker
from simulationentity import SimulationEntity


class Host(SimulationEntity):
    def parse_message(self, msg):
        pass

    def __init__(self, identity=0, ram=math.inf, processing_elements=None, fixed_task_finishing=8):
        super().__init__()
        self.id = identity
        self.ram = ram
        self.pes = processing_elements
        self.waiting_tasks = Queue()
        # To be moved to another host
        self.task_finishing_time = fixed_task_finishing
        self.dist = DistributionMaker()
        self.dist.get_address("ds.txt")
        self.coefficient_per_object = 1
        self.next_available_time = 0

    def estimate_task_time(self, packet, current_time):
        if packet.task.completed:
            return current_time + 0.04 * random() + 0.01
        # self.next_available_time = max(self.next_available_time, current_time)
        # self.next_available_time = self.next_available_time +\
        #        self.task_finishing_time + self.coefficient_per_object * packet.task.number_of_objects
        # return self.next_available_time
        return current_time + self.task_finishing_time + self.coefficient_per_object * packet.task.number_of_objects

    def add_task(self, task):
        pass

    def send_finished_tasks(self):
        pass