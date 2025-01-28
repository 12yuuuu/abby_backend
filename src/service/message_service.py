from fastapi import Depends
from src.core.schema import TablePageResp
from src.crud.message_crud import MessageCrud
from src.model.models import Message
from src.schema.message_schema import (
    MessageAddReq,
    MessageUpdateReq,
    MessagePageReq,
)


class MessageService:
    def __init__(self, message_crud: MessageCrud = Depends()) -> None:
        self._message_crud = message_crud

    def add_message(self, req: MessageAddReq) -> Message:
        message = Message(
            chat_id=req.chat_id, role=req.role, message_type=req.message_type, message_data=req.message_data
        )
        return self._message_crud.insert_entity(message)

    def update_message(self, id: int, req: MessageUpdateReq) -> Message:
        message = self._message_crud.select_by_id(id)
        message.chat_id = req.chat_id
        message.role = req.role
        message.message_type = req.message_type
        message.message_data = req.message_data
        return self._message_crud.update_entity(message)

    def delete_message(self, id: int) -> None:
        self._message_crud.delete_by_id(id)

    def get_message_page(self, req: MessagePageReq) -> TablePageResp:
        return self._message_crud.select_page(req, chat_id=req.chat_id, role=req.role)
