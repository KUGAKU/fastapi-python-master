from fastapi import APIRouter
from injector import Injector

from dimodules.sample_di import SampleDi
from presentation.sample_controller import SampleController
from schemas.sample import SampleRequest, SampleResponse

router = APIRouter()


@router.post("/", response_model=SampleResponse)
def sample(request: SampleRequest):
    injector = Injector([SampleDi()])
    sample_controller = injector.get(SampleController)
    response = sample_controller.sample(message=request.message)
    return SampleResponse(message=response["message"])
