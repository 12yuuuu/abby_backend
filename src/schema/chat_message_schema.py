from pydantic import BaseModel, Field
from src.core.schema import PageReq, TablePageResp


class ChatMessageAddReq(BaseModel):
    chat_id: int = Field(title="Chat ID", description="Unique identifier for a chat session")
    role: str = Field(title="Role", description="Role of the sender (e.g., user, abby)")
    message_type: str = Field(title="Message Type", description="Type of the message (e.g., text, image)")
    message_data: str = Field(title="Message Data", description="Content of the message")

class ChatMessageUpdateReq(ChatMessageAddReq):
    pass

class ChatMessageDetail(BaseModel):
    id: int = Field(title="Message ID")
    chat_id: int = Field(title="Chat ID")
    role: str = Field(title="Role")
    message_type: str = Field(title="Message Type")
    message_data: str = Field(title="Message Data")
    create_timestamp: int = Field(title="Creation Timestamp")


class ChatMessagePageReq(PageReq):
    chat_id: int = Field(default=None, title="Filter by Chat ID")
    role: str = Field(default=None, title="Filter by Role (user or abby)")
    message_type: str = Field(default=None, title="Filter by Message Type (text or image)")
    message_data: str = Field(default=None, title="Filter by Message Data (text content or file URL)")


class ChatMessagePageResp(TablePageResp):
    data: list[ChatMessageDetail] = Field(title="Messages Data")
