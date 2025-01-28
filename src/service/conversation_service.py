from fastapi import Depends
from src.core.schema import TablePageResp
from src.crud.conversation_crud import ConversationCrud
from src.model.models import Conversation
from src.schema.conversation_schema import (
    ConversationAddReq,
    ConversationUpdateReq,
    ConversationPageReq,
)


class ConversationService:
    def __init__(self, conversation_crud: ConversationCrud = Depends()) -> None:
        self._conversation_crud = conversation_crud

    def add_conversation(self, req: ConversationAddReq) -> Conversation:
        conversation = Conversation(
            tenant_id=req.tenant_id, bot_id=req.bot_id, title=req.title
        )
        return self._conversation_crud.insert_entity(conversation)

    def update_conversation(self, id: int, req: ConversationUpdateReq) -> Conversation:
        conversation = self._conversation_crud.select_by_id(id)
        conversation.tenant_id = req.tenant_id
        conversation.bot_id = req.bot_id
        conversation.title = req.title
        return self._conversation_crud.update_entity(conversation)

    def delete_conversation(self, id: int) -> None:
        self._conversation_crud.delete_by_id(id)

    def get_conversation_page(self, req: ConversationPageReq) -> TablePageResp:
        return self._conversation_crud.select_page(req, tenant_id=req.tenant_id, bot_id=req.bot_id)
