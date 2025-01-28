from pydantic import BaseModel, Field
from typing import List
from src.core.schema import PageReq, PageResp


class ClientAddReq(BaseModel):
    tenant_id: str | None = Field(default="", title="Tenant ID", max_length=32)
    openid: str | None = Field(default="", title="WeChat OpenID", max_length=64)
    follow_source: str | None = Field(default="", title="Follow Source", max_length=32)
    name: str | None = Field(default="", title="Client Name", max_length=50)
    age: int | None = Field(default=0, title="Client Age", ge=0, le=150)
    gender: str | None = Field(default="", title="Client Gender", max_length=8)
    email: str | None = Field(default="", title="Email Address")
    tel: str | None = Field(default="", title="Phone Number", max_length=16)
    address: str | None = Field(default="", title="Address", max_length=256)
    contact: str | None = Field(default="", title="Contact Person", max_length=50)
    qq: str | None = Field(default="", title="QQ Account", max_length=64)
    weibo: str | None = Field(default="", title="Weibo Account", max_length=64)
    weixin: str | None = Field(default="", title="WeChat Account", max_length=64)
    comment: str | None = Field(default="", title="Comment", max_length=500)


class ClientUpdateReq(ClientAddReq):
    pass


class ClientDetail(BaseModel):
    id: int = Field(title="Client ID")
    tenant_id: str | None = Field(default="", title="Tenant ID")
    openid: str | None = Field(default="", title="WeChat OpenID")
    follow_source: str | None = Field(default="", title="Follow Source")
    name: str | None = Field(default="", title="Client Name")
    age: int | None = Field(default=0, title="Client Age")
    gender: str | None = Field(default="", title="Client Gender")
    email: str | None = Field(default="", title="Email Address")
    tel: str | None = Field(default="", title="Phone Number")
    address: str | None = Field(default="", title="Address")
    contact: str | None = Field(default="", title="Contact Person")
    qq: str | None = Field(default="", title="QQ Account")
    weibo: str | None = Field(default="", title="Weibo Account")
    weixin: str | None = Field(default="", title="WeChat Account")
    comment: str | None = Field(default="", title="Comment")


class ClientPageReq(PageReq):
    tenant_id: str | None = Field(default="", title="Filter by Tenant ID")
    name: str | None = Field(default="", title="Filter by Name")
    gender: str | None = Field(default="", title="Filter by Gender")
    age: int | None = Field(default=0, title="Filter by Age")
    email: str | None = Field(default="", title="Filter by Email")
    tel: str | None = Field(default="", title="Filter by Phone Number")


class ClientPageResp(PageResp):
    data: List[ClientDetail] = Field(title="Client List")
