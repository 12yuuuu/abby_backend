from pydantic import BaseModel, Field

from src.core.schema import PageReq, PageResp


class UserAddReq(BaseModel):
    username: str = Field(title="Username")
    age: int = Field(title="Age", ge=0, le=200)


class UserDetail(BaseModel):
    id: int = Field(title="User ID")
    username: str = Field(title="Username")
    age: int = Field(title="Age")


class UserUpdateReq(BaseModel):
    username: str = Field(title="Username")
    age: int = Field(title="Age", ge=0, le=200)


class UserPageReq(PageReq):
    username: str | None = Field(default=None, title="Username", description="Fuzzy search")
    age: int | None = Field(default=None, title="Age")


class UserPageResp(PageResp):
    data: list[UserDetail] = Field(title="Data")
