import math
from random import random
from typing import List

from absgraph import AbstractGraph
from absqueue import AbstractPriorityQueue
from event import Event
from eventcodes import EventCodes
from game import Game
from heap import HeapQueue
from host import Host
from switch import Switch


class SimulationEngine:
    def __init__(self, games, topology, controller):
        self.event_queue: AbstractPriorityQueue = HeapQueue()
        self.topology: AbstractGraph = topology
        self.games: List[Game] = games
        self.controller = controller
        self.current_time = 0.0
        self.completed_tasks = []
        self.dropped_tasks = []
        self.controller.initialize(self.topology, self.games)

    def run_next_event(self):
        _, e = self.event_queue.poll()
        if e.code == EventCodes.PACKET_IN_NETWORK:
            self.controller.set_path(e.packet)
            device = self.topology.map(e.packet.go_to_next_hop())
            new_event = Event(EventCodes.PACKET_ARRIVED_SWITCH, self.current_time, self.current_time, e.packet, device)
            self.event_queue.add_item(new_event.end, new_event)
        elif e.code == EventCodes.PACKET_ARRIVED_SWITCH:
            time_in_queue = self.estimate_time_in_queue(e)
            if time_in_queue == -1:
                new_event = Event(EventCodes.PACKET_DROPPED, self.current_time, self.current_time, e.packet)
                self.event_queue.add_item(new_event.end, new_event)
            new_event = Event(EventCodes.PACKET_OUTSIDE_SWITCH_QUEUE, self.current_time,
                              self.current_time + time_in_queue, e.packet)
            self.event_queue.add_item(new_event.end, new_event)
        elif e.code == EventCodes.PACKET_OUTSIDE_SWITCH_QUEUE:
            # First none end time, second bandwidth object
            current_hop = e.device.id
            nxt_hop = e.packet.peek_next_hop()
            bandwidth = self.topology.get_outward_edges(current_hop)
            arrival_time = bandwidth.add_packet(e.packet, self.current_time)
            new_event = Event(EventCodes.PACKET_TRANSMITTED, self.current_time, arrival_time, e.packet, bandwidth)
            self.event_queue.add_item(new_event.end, new_event)
        elif e.code == EventCodes.PACKET_TRANSMITTED:
            bandwidth = e.device
            next_hop = self.topology.map(e.packet.go_to_next_hop())
            if isinstance(next_hop, Host):
                pass
            elif isinstance(next_hop, Switch):
                pass
            else:
                # datacenter gateway
                pass

        elif e.code == EventCodes.PACKET_ARRIVED_HOST:
            h:Host = e.device
            processing_time = h.estimate_task_time(e.task)
            new_event = Event(EventCodes.PACKET_PROCESS_FINISHED, self.current_time, self.current_time + processing_time
                              , e.packet)
            self.event_queue.add_item(new_event.end, new_event)
        elif e.code == EventCodes.PACKET_PROCESS_FINISHED:
            pass
        elif e.code == EventCodes.PACKET_LEFT_DATACENTER:
            self.completed_tasks.append(e.packet)
        elif e.code == EventCodes.PACKET_DROPPED:
            self.dropped_tasks.append(e.packet)
        else:
            # unknown event
            pass

    def start(self, stop_time=math.inf):
        while self.current_time <= stop_time:
            self.add_new_events()
            self.run_next_event()

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
            events = g.generate_events(self.current_time)
            for e in events:
                self.event_queue.add_item(e.end, e)

    def estimate_time_in_queue(self, e):
        sw: Switch = e.device
        sz = sw.packet_queue.qsize()
        if sz == sw.max_size:
            return 0.004 * random() + 0.001
        return (sz+1) * sw.sending_packet_time

    def estimate_processing_time(self, e: Event):
        host: Host = e.device
        t = host.estimate_task_time(e.packet.task)
        host.add_task(e.packet.task)
        return t
