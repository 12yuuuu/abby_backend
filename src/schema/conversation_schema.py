from pydantic import BaseModel, Field
from typing import List
from src.core.schema import PageReq, PageResp


class ConversationAddReq(BaseModel):
    tenant_id: str = Field(title="Tenant ID")
    bot_id: int = Field(title="Bot ID")
    title: str = Field(title="Conversation Title")


class ConversationUpdateReq(ConversationAddReq):
    pass


class ConversationDetail(BaseModel):
    id: int = Field(title="Conversation ID")
    tenant_id: str = Field(title="Tenant ID")
    bot_id: int = Field(title="Bot ID")
    title: str = Field(title="Conversation Title")


class ConversationPageReq(PageReq):
    tenant_id: str | None = Field(default=None, title="Filter by Tenant ID")
    bot_id: int | None = Field(default=None, title="Filter by Bot ID")


class ConversationPageResp(PageResp):
    data: List[ConversationDetail] = Field(title="Conversation List")