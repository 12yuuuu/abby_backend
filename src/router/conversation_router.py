from fastapi import APIRouter, Query, Path, Body, Depends
from src.core.schema import SuccessResp
from src.schema.conversation_schema import (
    ConversationAddReq,
    ConversationUpdateReq,
    ConversationDetail,
    ConversationPageReq,
    ConversationPageResp,
)
from src.service.conversation_service import ConversationService

router = APIRouter(prefix="/conversation", tags=["Conversation Management"])


@router.get("", summary="Get conversation list", response_model=ConversationPageResp)
def get_conversation_page(
    req: ConversationPageReq = Query(),
    service: ConversationService = Depends(),
):
    return service.get_conversation_page(req)


@router.post("", summary="Add conversation", response_model=ConversationDetail)
def add_conversation(req: ConversationAddReq, service: ConversationService = Depends()):
    return service.add_conversation(req)


@router.put("/{id}", summary="Update conversation", response_model=ConversationDetail)
def update_conversation(
    id: int = Path(), req: ConversationUpdateReq = Body(), service: ConversationService = Depends()
):
    return service.update_conversation(id, req)


@router.delete("/{id}", summary="Delete conversation", response_model=SuccessResp)
def delete_conversation(id: int = Path(), service: ConversationService = Depends()):
    service.delete_conversation(id)
    return SuccessResp()
