from pydantic import BaseModel, Field
from typing import List
from src.core.schema import PageReq, PageResp


class CustomerAddReq(BaseModel):
    name: str = Field(title="Customer Name")
    age: int = Field(title="Customer Age", ge=0)
    gender: str = Field(title="Customer Gender")


class CustomerUpdateReq(CustomerAddReq):
    pass


class CustomerDetail(BaseModel):
    id: int = Field(title="Customer ID")
    name: str = Field(title="Customer Name")
    age: int = Field(title="Customer Age")
    gender: str = Field(title="Customer Gender")


class CustomerPageReq(PageReq):
    name: str | None = Field(default=None, title="Filter by Name")
    age: int | None = Field(default=None, title="Filter by Age")
    gender: str | None = Field(default=None, title="Filter by Gender")


class CustomerPageResp(PageResp):
    data: List[CustomerDetail] = Field(title="Customer List")
