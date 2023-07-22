from pydantic import BaseModel


class SampleResponse(BaseModel):
    message: str


class SampleRequest(BaseModel):
    message: str
