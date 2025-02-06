from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from decimal import Decimal
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
                # Try to parse the string as JSON
                return json.loads(v)
            except json.JSONDecodeError:
                return v  # If parsing fails, return the original string
        # Convert Decimal to float for JSON serialization
        if isinstance(v, list):
            return [{k: (float(val) if isinstance(val, Decimal) else val) for k, val in item.items()} for item in v]
        return v