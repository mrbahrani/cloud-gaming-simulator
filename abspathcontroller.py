from controller import Controller


class AbstractPathController(Controller):
    def set_path(self, packet):
        raise NotImplementedError

    def preprocess(self):
        pass

    def get_feedback(self, packet):
        pass