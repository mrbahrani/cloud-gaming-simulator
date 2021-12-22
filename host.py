import math
from queue import Queue

from simulationentity import SimulationEntity


class Host(SimulationEntity):
    def parse_message(self, msg):
        pass

    def __init__(self, identity=0, ram=math.inf, processing_elements={}):
        super().__init__()
        self.id = identity
        self.ram = ram
        self.pes = processing_elements
        self.waiting_tasks = Queue()
        # To be moved to another host
        self.task_finishing_time = 1

    def estimate_task_time(self, task):
        # This is the easiest way to simulate should be changed
        return self.task_finishing_time

    def add_task(self, task):
        pass

    def send_finished_tasks(self):
        pass