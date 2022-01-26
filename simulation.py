import math
from random import random
from typing import List

import numpy as np

from absgraph import AbstractGraph
from absqueue import AbstractPriorityQueue
from event import Event
from eventcodes import EventCodes
from game import Game
from heap import HeapQueue
from host import Host
from packet import Packet
from switch import Switch
from matplotlib import pyplot as plt


class SimulationEngine:
    def __init__(self, games, topology, controller):
        self.event_queue: AbstractPriorityQueue = HeapQueue()
        self.topology: AbstractGraph = topology
        self.games: List[Game] = games
        self.controller = controller
        self.current_time = 0.0
        self.completed_tasks = []
        self.dropped_tasks = []
        # self.controller.initialize(self.topology, self.games)
        self.controller.initialize(self.topology)

    def run_next_event(self):
        _, e = self.event_queue.poll()
        self.current_time = e.end
        e.packet.history.append([self.current_time, e.device])
        if e.code == EventCodes.PACKET_IN_NETWORK:
            # e.packet.start = self.current_time
            self.controller.set_path(e.packet)
            device = self.topology.map(e.packet.go_to_next_hop())
            new_event = Event(EventCodes.PACKET_ARRIVED_SWITCH, self.current_time, self.current_time, e.packet, device)
            self.event_queue.add_item(new_event.end, new_event)
        elif e.code == EventCodes.PACKET_ARRIVED_SWITCH:
            e.packet.packets_ahead = e.device.packet_queue.qsize()
            time_in_queue = self.estimate_time_in_queue(e)
            if time_in_queue == -1:
                new_event = Event(EventCodes.PACKET_DROPPED, self.current_time, self.current_time, e.packet, e.device)
                self.event_queue.add_item(new_event.end, new_event)
                return
            sw: Switch = e.device
            sw.receive(e.packet)
            new_event = Event(EventCodes.PACKET_OUTSIDE_SWITCH_QUEUE, self.current_time,
                              self.current_time + time_in_queue, e.packet, e.device)
            self.event_queue.add_item(new_event.end, new_event)
        elif e.code == EventCodes.PACKET_OUTSIDE_SWITCH_QUEUE:
            e.packet.packets_ahead = 0
            current_hop: Switch = self.topology.map(e.device.id)
            nxt_hop = e.packet.peek_next_hop()
            bandwidth = self.topology.get_edge_properties(current_hop, nxt_hop)["bandwidth"]
            arrival_time = bandwidth.add_packet(e.packet, self.current_time)
            new_event = Event(EventCodes.PACKET_TRANSMITTED, self.current_time, arrival_time, e.packet, bandwidth)
            self.event_queue.add_item(new_event.end, new_event)
            current_hop.send()
        elif e.code == EventCodes.PACKET_TRANSMITTED:
            next_hop = self.topology.map(e.packet.go_to_next_hop())
            if isinstance(next_hop, Host):
                new_event = Event(EventCodes.PACKET_ARRIVED_HOST, self.current_time, self.current_time, e.packet,
                                  next_hop)
            elif isinstance(next_hop, Switch):
                new_event = Event(EventCodes.PACKET_ARRIVED_SWITCH, self.current_time, self.current_time, e.packet,
                                  next_hop)
            else:
                new_event = Event(EventCodes.PACKET_LEFT_DATACENTER, self.current_time, self.current_time, e.packet,
                                  next_hop)
            self.event_queue.add_item(new_event.end, new_event)
        elif e.code == EventCodes.PACKET_ARRIVED_HOST:
            h: Host = e.device
            processing_time = h.estimate_task_time(e.packet, self.current_time)
            new_event = Event(EventCodes.PACKET_PROCESS_FINISHED, self.current_time, processing_time
                              , e.packet, e.device)
            self.event_queue.add_item(new_event.end, new_event)
        elif e.code == EventCodes.PACKET_PROCESS_FINISHED:
            e.packet.task.completed = True
            current_hop = e.device.id
            nxt_hop = e.packet.peek_next_hop()
            bandwidth = self.topology.get_edge_properties(current_hop, nxt_hop)["bandwidth"]
            arrival_time = bandwidth.add_packet(e.packet, self.current_time)
            new_event = Event(EventCodes.PACKET_TRANSMITTED, self.current_time, arrival_time, e.packet, bandwidth)
            self.event_queue.add_item(new_event.end, new_event)
        elif e.code == EventCodes.PACKET_LEFT_DATACENTER:
            e.packet.end = self.current_time + e.packet.player.reach_out_time
            try:
                e.packet.extras[1] = e.packet.end - e.packet.start
            except:
                pass
            self.controller.get_feedback(e.packet)
            self.completed_tasks.append(e.packet)
        elif e.code == EventCodes.PACKET_DROPPED:
            self.dropped_tasks.append(e.packet)
        else:
            # unknown event
            pass

    def start(self, stop_time=math.inf):
        self.add_game_events(stop_time)
        while self.current_time <= stop_time and not self.event_queue.empty():
            self.run_next_event()

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

    def create_report(self):
        results = dict()
        results["paket_loss"] = len(self.dropped_tasks) / (len(self.dropped_tasks) + len(self.completed_tasks))
        results["timeliness"] = len(list(filter(lambda x: (x.end-x.start) < x.timeout, self.completed_tasks))) / \
                                len(self.completed_tasks)
        delays = np.array(list(map(lambda p: p.end - p.start, self.completed_tasks)))
        results["delay_average"] = delays.mean()
        results["delay_sd"] = delays.std()
        results["delay_score"] = np.array(list(map(lambda p: p.timeout - (p.end - p.start), self.completed_tasks))).mean()
        bws = []
        for node_list in self.topology.adj_list:
            for item in self.topology.adj_list[node_list]:
                bw = item[2]["bandwidth"]
                bws.append(bw)
        active_bws = list(filter(lambda x: x.active_time != 0, bws))
        results["active_rate"] = len(active_bws) / len(bws)
        utilizations = np.array(list(map(lambda x: x.get_utilization(), bws)))
        results["bw_mean"] = utilizations.mean()
        results["bw_std"] = utilizations.std()

        d_scores = np.array(list(map(lambda p: p.timeout - (p.end - p.start), self.completed_tasks)))
        results["min_d_score"] = d_scores.min()
        results["max_d_score"] = d_scores.max()

        results["delays_q1"] = np.percentile(d_scores, 25)
        results["delays_q2"] = np.percentile(d_scores, 50)
        results["delays_q3"] = np.percentile(d_scores, 75)

        results["min_d_score"] = d_scores.min()
        results["max_d_score"] = d_scores.max()

        results["d_score_q1"] = np.percentile(d_scores, 25)
        results["d_score_q2"] = np.percentile(d_scores, 50)
        results["d_score_q3"] = np.percentile(d_scores, 75)




        # show plot
        # plt.show()
        for p in self.completed_tasks:
            # print("packet", p.start, p.end, p.end - p.start, p.timeout)
            pass
        print(results)
        return results

    def add_game_events(self, stop_time):
        for g in self.games:
            events = g.generate_events(stop_time)
            for e in events:
                self.event_queue.add_item(e.end, e)

    def estimate_time_in_queue(self, e):
        sw: Switch = e.device
        sz = sw.queue_size
        if sz >= sw.max_size:
            return -1
        return (sz+1) * sw.sending_packet_time

    def estimate_processing_time(self, e: Event):
        host: Host = e.device
        t = host.estimate_task_time(e.packet)
        host.add_task(e.packet.task)
        return t
