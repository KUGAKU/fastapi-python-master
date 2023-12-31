from abc import ABC, abstractmethod

from injector import inject

from business_logic.sample_service import AbstractSampleService


class AbstractSampleController(ABC):
    @abstractmethod
    def sample(self, message: str) -> dict:
        raise NotImplementedError()


class SampleController(AbstractSampleController):
    @inject
    def __init__(self, sampleService: AbstractSampleService) -> None:
        if not isinstance(sampleService, AbstractSampleService):
            raise TypeError(
                "sampleService must be an instance of AbstractSampleService"
            )
        self.sampleService = sampleService

    def sample(self, message: str) -> dict:
        return self.sampleService.sample(message=message)
