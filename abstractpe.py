from abc import ABC


class AbstractProcessingElement(ABC):
    def add_task(self, task):
        raise NotImplementedError

    def release_finished_tasks(self):
        raise NotImplementedError
