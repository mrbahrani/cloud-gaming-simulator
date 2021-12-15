class Packet:
    def __init__(self, identity, player, game, timeout, task):
        self.id = identity
        self.player = player
        self.game = game
        self.timout = timeout
        self.task = task
        self.history = dict()
        self.path = None

    def set_path(self, path):
        self.path = path
