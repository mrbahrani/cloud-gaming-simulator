class Event:
    def __init__(self, code,  start, end, packet):
        self.code = code
        self.start = 0
        self.end = 0
        self.packet = packet
        self.device = None