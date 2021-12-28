class Event:
    def __init__(self, code,  start, end, packet, device=None):
        self.code = code
        self.start = start
        self.end = end
        self.packet = packet
        self.device = device
