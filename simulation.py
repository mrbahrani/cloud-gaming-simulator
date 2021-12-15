import math
from typing import List

from absqueue import AbstractPriorityQueue
from event import Event
from game import Game
from heap import HeapQueue


class SimulationEngine:
    def __init__(self, games, topology, controller):
        self.event_queue: AbstractPriorityQueue = HeapQueue()
        self.topology = topology
        self.games: List[Game] = games
        self.controller = controller
        self.current_time = 0.0
        self.completed_tasks = []

    def run_next_event(self):
        _, e = self.event_queue.poll()
        # ToDo run event
        # Test create another event
        e = Event()
        e.end = self.current_time + 5
        self.event_queue.add_item(e.end, e)
        return e

    def start(self, stop_time=math.inf):
        while self.current_time <= stop_time:
            self.add_new_events()
            e: Event = self.run_next_event()
            self.current_time = e.end
            print(self.current_time)

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

    def create_report(self):
        # ToDo implement it!
        pass

    def add_new_events(self):
        for g in self.games:
            events = g.generate_events()
            for e in events:
                self.event_queue.add_item(e.end, e)
