class Event:
    def __init__(self, code,  start, end, packet, device=None):
        self.code = code
        self.start = 0
        self.end = 0
        self.packet = packet
        self.device = device
