from fastapi import APIRouter, Query, Depends
from src.schema.agent_schema import (
    AgentAddReq,
    AgentDetail,
    AgentPageReq,
    AgentPageResp,
)
from src.service.agent_service import AgentService

router = APIRouter(prefix="/agent", tags=["Agent Management"])


@router.get("", summary="Get agent records", response_model=AgentPageResp)
def get_agent_page(
    req: AgentPageReq = Query(),
    service: AgentService = Depends(),
):
    return service.get_agent_page(req)

@router.get("/{id}", summary="Get agent by ID", response_model=AgentDetail)
def get_agent(
    id: int,
    service: AgentService = Depends()
):
    return service.get_agent(id)


@router.post("", summary="Add agent record", response_model=AgentDetail)
def add_agent(
    req: AgentAddReq, 
    service: AgentService = Depends()
):
    return service.add_agent(req)