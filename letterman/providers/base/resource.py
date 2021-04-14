from abc import abstractmethod


class Resource:
    @abstractmethod
    async def get(self):
        raise NotImplementedError()

    @abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def destroy(self):
        raise NotImplementedError()
