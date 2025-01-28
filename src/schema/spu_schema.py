from pydantic import BaseModel, Field
from typing import List
from src.core.schema import PageReq, PageResp


class SpuAddReq(BaseModel):
    title: str = Field(title="SPU Title")
    brand: str | None = Field(default=None, title="Brand")


class SpuUpdateReq(SpuAddReq):
    pass


class SpuDetail(BaseModel):
    id: int = Field(title="SPU ID")
    title: str = Field(title="SPU Title")
    brand: str | None = Field(default=None, title="Brand")


class SpuPageReq(PageReq):
    title: str | None = Field(default=None, title="Filter by Title")
    brand: str | None = Field(default=None, title="Filter by Brand")


class SpuPageResp(PageResp):
    data: List[SpuDetail] = Field(title="SPU List")