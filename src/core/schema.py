from typing import Any
from pydantic import BaseModel, Field

class PageReq(BaseModel):
    """Pagination parameters

    The base class for pagination query models, such as class UserPageQry(PageQry)
    """

    page_index: int = Field(example=1, ge=1, title="Page Number", description="Starts from 1")
    page_size: int = Field(
        example=10,
        ge=1,
        le=100,
        title="Page Size",
        description="Range 1-100 (values too large may affect performance)",
    )

    def get_offset(self) -> int:
        """Get the starting position

        Returns:
            int: Index value
        """
        return self.page_size * (self.page_index - 1)

    def get_limit(self) -> int:
        """Get the page size

        Returns:
            int: Page size
        """
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
    data: list[Any] = Field(title="Data")


class LoginUser(BaseModel):
    """Logged-in user"""

    tenant_id: str = Field(title="Tenant ID")
    user_id: int = Field(title="User ID")
