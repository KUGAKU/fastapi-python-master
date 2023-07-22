from fastapi import APIRouter
from injector import Injector

from dimodules.sample_di import SampleDi
from presentation.sample_controller import SampleController
from schemas.sample import SampleResponse

router = APIRouter()

@router.get("/", response_model=SampleResponse)
def retrieve_sample_message():
    injector = Injector([SampleDi()])
    sample_controller = injector.get(SampleController)
    response = sample_controller.sample()
    return SampleResponse(message=response["message"])

