from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from src.core.schema import PageReq, PageResp
import json

class AgentAddReq(BaseModel):
    query: str = Field(title="User Query")

class AgentDetail(BaseModel):
    id: Optional[int] = Field(title="Agent ID")
    analysis: Optional[str] = Field(default=None, title="LLM Analysis")
    data: Optional[List[Dict[str, Any]]] = Field(default=None, title="Analysis Data")

    @validator('data', pre=True)
    def parse_data(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return v
        return v

class AgentPageReq(PageReq):
    pass  # No additional filters needed

class AgentPageResp(PageResp):
    data: List[AgentDetail] = Field(title="List of Agent Records")