from abc import ABC, abstractmethod

from models.sample import Sample
from settings import Session


class AbstractSampleRepository(ABC):

    @abstractmethod
    def sample(self, message: str) -> dict:
        raise NotImplementedError()


class SampleRepository(AbstractSampleRepository):
    def __init__(self) -> None:
        pass

    def sample(self, message: str) -> dict:
        session = Session()
        try:
            sample = Sample()
            sample.data = message
            session.add(sample)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()
        return {"message": "success to create " + message}
