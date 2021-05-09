from abc import abstractmethod

from datetime import datetime

from letterman.providers.base.resource import Resource


class Instance(Resource):
    """
    The class is merely a container of data. Based off this data the instance the state of the instance can be modified,
    but the right data needs to be present for certain actions. E.g. to start an instance you only need an identifier
    but the creation of an instance requires much more data.
    """
    def __init__(self, response):
        self.properties = {}
        self.update_properties(response)

    @property
    def get_instance_id(self) -> str:
        return self.properties.get("id")

    @property
    def get_instance_state(self) -> str:
        return self.properties.get("state")

    @property
    def get_public_ip(self) -> str:
        return self.properties.get("public_ip")

    @property
    def get_game(self) -> str:
        return self.properties.get("game")

    @property
    def get_name(self) -> str:
        return self.properties.get("name")

    def update_properties(self, properties: dict) -> None:
        if not properties:
            return {}
        for key, value in properties.items():
            self.properties[key] = value
        self.properties["updated"] = datetime.now().isoformat()

    def describe(self) -> dict:
        return self.properties

    @abstractmethod
    async def start(self) -> dict:
        raise NotImplementedError()

    @abstractmethod
    async def stop(self) -> dict:
        raise NotImplementedError()

    @abstractmethod
    async def create(self) -> dict:
        raise NotImplementedError()

    @abstractmethod
    async def destroy(self) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def _parse_api_response(self, response: dict) -> dict:
        raise NotImplementedError()
