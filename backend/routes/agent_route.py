from fastapi import APIRouter
from pydantic import BaseModel

from services.graph import graph


router = APIRouter()


class RequestBody(BaseModel):
    message: str


@router.post("/agent")
def agent_route(request: RequestBody):

    response = graph.invoke({
        "input": request.message
    })

    return response