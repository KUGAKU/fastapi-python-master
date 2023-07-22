from fastapi import APIRouter

from schemas.echo import EchoResponse

router = APIRouter()

@router.get("/{echo_string}", response_model=EchoResponse)
def echo(echo_string: str):
    return EchoResponse(message=echo_string)

@router.get("/fixed")
def fixed_echo():
    return {"message": "fixed"}
