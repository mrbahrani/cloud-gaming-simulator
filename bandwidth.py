import math

from event import Event
from eventcodes import EventCodes


class Bandwidth:
    def __init__(self, rate=10, cap=math.inf):
        self.cap = cap
        self.rate = rate
        self.last_update_time = 0
        self.active_time = 0
        self.is_active = False
        self.bytes_transmitted = 0
        self.queue = []

    def update(self, current_time):
        if self.is_active:
            passed_time = current_time - self.last_update_time
            potential_transmitted_bytes = passed_time * self.rate
            left_bytes = potential_transmitted_bytes
            actually_transmitted_bytes = 0
            while left_bytes > 0:
                if len(self.queue) == 0:
                    self.is_active = False
                    break
                tq = self.queue[0]
                if tq[1] > left_bytes:
                    actually_transmitted_bytes += left_bytes
                    self.queue[0][1] -= left_bytes
                    left_bytes = 0
                elif tq[1] == left_bytes:
                    actually_transmitted_bytes += left_bytes
                    self.queue[0][1] -= left_bytes
                    left_bytes = 0
                    self.queue.pop(0)
                else:
                    actually_transmitted_bytes += self.queue[0][1]
                    left_bytes -= self.queue[0][1]
                    self.queue[0][1] = 0
                    self.queue.pop(0)
            if potential_transmitted_bytes == 0:
                return
            self.active_time += (actually_transmitted_bytes/ potential_transmitted_bytes) * passed_time
        self.last_update_time = current_time

    def get_utilization(self):
        if self.active_time == 0:
            return 1
        return self.bytes_transmitted / (self.active_time * self.rate)

    def add_packet(self, packet, current_time):
        self.is_active = True
        self.update(current_time)
        self.queue.append([packet, packet.length])
        time_to_arrive = sum(map(lambda x: x[1], self.queue)) / self.rate
        return current_time + time_to_arrive




