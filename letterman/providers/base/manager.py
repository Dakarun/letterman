from abc import abstractmethod


class Manager(object):
    @abstractmethod
    def list(self):
        raise NotImplementedError()
