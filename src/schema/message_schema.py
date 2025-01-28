from pydantic import BaseModel, Field
from typing import List
from src.core.schema import PageReq, PageResp


class MessageAddReq(BaseModel):
    chat_id: int = Field(title="Chat ID")
    role: str = Field(title="Role")
    message_type: str = Field(title="Message Type")
    message_data: str = Field(title="Message Data")


class MessageUpdateReq(MessageAddReq):
    pass


class MessageDetail(BaseModel):
    id: int = Field(title="Message ID")
    chat_id: int = Field(title="Chat ID")
    role: str = Field(title="Role")
    message_type: str = Field(title="Message Type")
    message_data: str = Field(title="Message Data")


class MessagePageReq(PageReq):
    chat_id: int | None = Field(default=None, title="Filter by Chat ID")
    role: str | None = Field(default=None, title="Filter by Role")


class MessagePageResp(PageResp):
    data: List[MessageDetail] = Field(title="Message List")