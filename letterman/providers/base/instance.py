from abc import abstractmethod

from letterman.providers.base.resource import Resource


class Instance(Resource):
    def __init__(self, name: str, game: str, public_ip=None):
        super().__init__()
        self.name = name
        self.game = game
        self.public_ip = public_ip
        self.instance_id = self._get_instance_id()
        self.state = self._get_instance_state()

    @abstractmethod
    def _get_instance_id(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _get_instance_state(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def start(self) -> dict:
        raise NotImplementedError()

    @abstractmethod
    async def stop(self) -> dict:
        raise NotImplementedError()
