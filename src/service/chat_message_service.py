from fastapi import Depends
from src.crud.chat_message_crud import ChatMessageCrud
from src.model.models import ChatMessage
from src.schema.chat_message_schema import ChatMessageAddReq, ChatMessagePageReq, ChatMessageUpdateReq
from src.core.schema import TablePageResp


class ChatMessageService:
    def __init__(self, chat_message_crud: ChatMessageCrud = Depends()) -> None:
        self._chat_message_crud = chat_message_crud

    def add_message(self, req: ChatMessageAddReq) -> ChatMessage:
        message = ChatMessage(
            chat_id=req.chat_id,
            role=req.role,
            message_type=req.message_type,
            message_data=req.message_data,
        )
        return self._chat_message_crud.insert_entity(message)
    
    def update_chat_message(self, id: int, req: ChatMessageUpdateReq) -> ChatMessage:
        chat_message = self._chat_message_crud.select_by_id(id)
        chat_message.role = req.role
        chat_message.message_type = req.message_type
        chat_message.message_data = req.message_data
        return self._chat_message_crud.update_entity(chat_message)

    def delete_message(self, id: int) -> None:
        self._chat_message_crud.delete_by_id(id)

    def get_message_page(self, req: ChatMessagePageReq) -> TablePageResp:
        return self._chat_message_crud.select_page(
            req,
            chat_id=req.chat_id,
            role=req.role,
            message_type=req.message_type,
        )
