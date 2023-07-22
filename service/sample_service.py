from abc import ABC, abstractmethod

from injector import inject
from repository.sample_repository import AbstractSampleRepository

class AbstractSampleService(ABC):
    @abstractmethod
    def sample(self) -> dict:
        raise NotImplementedError()

class SampleService(AbstractSampleService):
    @inject
    def __init__(self, sample_repository: AbstractSampleRepository) -> None:
        if not isinstance(sample_repository, AbstractSampleRepository):
            raise TypeError("sample_repository must be an instance of AbstractSampleRepository")
        self.sample_repository = sample_repository

    def sample(self) -> dict:
        return self.sample_repository.sample()
