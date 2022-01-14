class Packet:
    def __init__(self, identity, player, game, l, timeout, task, typ='res'):
        self.id = identity
        self.player = player
        self.game = game
        self.timout = timeout
        self.task = task
        self.length = l
        self.type = typ
        self.history = []
        self.path = None
        self.current_next_hop = 0
        self.start = 0
        self.end = 0
        self.packets_ahead = 0
        self.extras = None

    def set_path(self, path):
        self.path = path

    def go_to_next_hop(self):
        self.current_next_hop += 1
        return self.path[self.current_next_hop]

    def peek_next_hop(self):
        return self.path[self.current_next_hop+1]


