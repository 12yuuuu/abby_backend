from fastapi import APIRouter, Query, Path, Body, Depends
from src.core.schema import SuccessResp
from src.schema.client_schema import (
    ClientAddReq,
    ClientUpdateReq,
    ClientDetail,
    ClientPageReq,
    ClientPageResp,
)
from src.service.client_service import ClientService

router = APIRouter(prefix="/client", tags=["Client Management"])

@router.get("", summary="Get client list", response_model=ClientPageResp)
def get_client_page(
    req: ClientPageReq = Query(),
    service: ClientService = Depends(),
):
    return service.get_client_page(req)


@router.post("", summary="Add client", response_model=ClientDetail)
def add_client(req: ClientAddReq, service: ClientService = Depends()):
    return service.add_client(req)


@router.put("/{id}", summary="Update client", response_model=ClientDetail)
def update_client(
    id: int = Path(), req: ClientUpdateReq = Body(), service: ClientService = Depends()
):
    return service.update_client(id, req)


@router.delete("/{id}", summary="Delete client", response_model=SuccessResp)
def delete_client(id: int = Path(), service: ClientService = Depends()):
    service.delete_client(id)
    return SuccessResp()