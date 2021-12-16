class Packet:
    def __init__(self, identity, player, game, l, timeout, task, typ='res'):
        self.id = identity
        self.player = player
        self.game = game
        self.timout = timeout
        self.task = task
        self.length = l
        self.type = typ
        self.history = dict()
        self.path = None

    def set_path(self, path):
        self.path = path

    def next_hop(self):
        pass

