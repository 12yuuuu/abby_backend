from fastapi import APIRouter, Query, Path, Body, Depends
from src.core.schema import SuccessResp
from src.schema.message_schema import (
    MessageAddReq,
    MessageUpdateReq,
    MessageDetail,
    MessagePageReq,
    MessagePageResp,
)
from src.service.message_service import MessageService

router = APIRouter(prefix="/message", tags=["Message Management"])


@router.get("", summary="Get message list", response_model=MessagePageResp)
def get_message_page(
    req: MessagePageReq = Query(),
    service: MessageService = Depends(),
):
    return service.get_message_page(req)


@router.post("", summary="Add message", response_model=MessageDetail)
def add_message(req: MessageAddReq, service: MessageService = Depends()):
    return service.add_message(req)


@router.put("/{id}", summary="Update message", response_model=MessageDetail)
def update_message(
    id: int = Path(), req: MessageUpdateReq = Body(), service: MessageService = Depends()
):
    return service.update_message(id, req)


@router.delete("/{id}", summary="Delete message", response_model=SuccessResp)
def delete_message(id: int = Path(), service: MessageService = Depends()):
    service.delete_message(id)
    return SuccessResp()