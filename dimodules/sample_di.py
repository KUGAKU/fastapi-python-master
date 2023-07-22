from injector import Binder, Module

from repository.sample_repository import AbstractSampleRepository, SampleRepository
from service.sample_service import AbstractSampleService, SampleService


class SampleDi(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(AbstractSampleRepository, to=SampleRepository)#type: ignore
        binder.bind(AbstractSampleService, to=SampleService)#type: ignore
