from abc import ABC, abstractmethod

from injector import inject

from data_access.sample_repository import AbstractSampleRepository


class AbstractSampleService(ABC):
    @abstractmethod
    def sample(self, message: str) -> dict:
        raise NotImplementedError()


class SampleService(AbstractSampleService):
    @inject
    def __init__(self, sample_repository: AbstractSampleRepository) -> None:
        if not isinstance(sample_repository, AbstractSampleRepository):
            raise TypeError(
                "sample_repository must be an instance of AbstractSampleRepository"
            )
        self.sample_repository = sample_repository

    def sample(self, message: str) -> dict:
        return self.sample_repository.sample(message=message)
