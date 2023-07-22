from abc import ABC, abstractmethod


class AbstractSampleRepository(ABC):

    @abstractmethod
    def sample(self) -> dict:
        raise NotImplementedError()


class SampleRepository(AbstractSampleRepository):
    def __init__(self) -> None:
        pass

    def sample(self) -> dict:
        return {"message": "sample"}

