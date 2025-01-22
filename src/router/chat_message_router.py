from fastapi import APIRouter, Path, Query, Body, Depends
from src.schema.chat_message_schema import (
    ChatMessageAddReq,
    ChatMessageUpdateReq,
    ChatMessageDetail,
    ChatMessagePageReq,
    ChatMessagePageResp,
)
from src.service.chat_message_service import ChatMessageService
from src.core.schema import SuccessResp

router = APIRouter(prefix="/chat_message", tags=["Chat Message Management"])


@router.get("", summary="Get chat messages list", response_model=ChatMessagePageResp)
def get_message_page(
    req: ChatMessagePageReq = Query(),
    service: ChatMessageService = Depends(),
):
    return service.get_message_page(req)


@router.post("", summary="Add chat message", response_model=ChatMessageDetail)
def add_message(req: ChatMessageAddReq, service: ChatMessageService = Depends()):
    return service.add_message(req)


@router.put("/{id}", summary="Update chat message", response_model=ChatMessageDetail)
def update_chat_message(
    id: int = Path(), req: ChatMessageUpdateReq = Body(), service: ChatMessageService = Depends()
):
    return service.update_chat_message(id, req)


@router.delete("/{id}", summary="Delete chat message", response_model=SuccessResp)
def delete_message(id: int = Path(), service: ChatMessageService = Depends()):
    service.delete_message(id)
    return SuccessResp()
