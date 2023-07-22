from fastapi import APIRouter
from injector import Injector

from dimodules.sample_di import SampleDi
from presentation.sample_controller import SampleController

router = APIRouter()

@router.get("/")
def retrieve_sample_items():
    injector = Injector([SampleDi()])
    sample_controller = injector.get(SampleController)
    return sample_controller.sample()

