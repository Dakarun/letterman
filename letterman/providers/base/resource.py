from abc import abstractmethod


class Resource:
    """
    Resources are meant to be containers of data. Based off the data present methods can be called to change the state
    of the resource.

    Based off this the constructor would not require any args.

    Public methods should return the latest state of the resource
    """
    @abstractmethod
    async def describe(self):
        raise NotImplementedError()

    @abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def destroy(self):
        raise NotImplementedError()
