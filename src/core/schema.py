from typing import Any, List, Optional
from pydantic import BaseModel, Field


class PageReq(BaseModel):
    """Pagination parameters"""

    page_index: int = Field(example=1, ge=1, title="Page Number", description="Starts from 1")
    page_size: int = Field(
        example=10,
        ge=1,
        le=100,
        title="Page Size",
        description="Range 1-100 (values too large may affect performance)",
    )

    def get_offset(self) -> int:
        """Get the starting position"""
        return self.page_size * (self.page_index - 1)

    def get_limit(self) -> int:
        """Get the page size"""
        return self.page_size


class SuccessResp(BaseModel):
    """Success response model"""

    message: str = Field("success", title="Message")


class ErrorResp(BaseModel):
    """Error response model"""

    summary: str = Field("Error Summary", title="Error Summary")
    message: str = Field("Error Message", title="Error Message")
    data: Any = Field(None, title="Data")


class PageResp(BaseModel):
    """Pagination response model"""

    page_index: int = Field(title="Page Number", description="Starts from 1")
    page_size: int = Field(title="Page Size")
    total_count: int = Field(title="Total Data Count")


class TablePageResp(BaseModel):
    """Data table response"""

    page_index: int = Field(title="Page Number", description="Starts from 1")
    page_size: int = Field(title="Page Size")
    total_count: int = Field(title="Total Data Count")
    data: List[Any] = Field(title="Data")



