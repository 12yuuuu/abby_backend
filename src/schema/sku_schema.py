from pydantic import BaseModel, Field
from typing import List
from src.core.schema import PageReq, PageResp


class SkuAddReq(BaseModel):
    spu_id: int = Field(title="SPU ID")
    sku_code: str = Field(title="SKU Code")
    initial_price: float = Field(title="Initial Price", ge=0)


class SkuUpdateReq(SkuAddReq):
    pass


class SkuDetail(BaseModel):
    id: int = Field(title="SKU ID")
    spu_id: int = Field(title="SPU ID")
    sku_code: str = Field(title="SKU Code")
    initial_price: float = Field(title="Initial Price")


class SkuPageReq(PageReq):
    spu_id: int | None = Field(default=None, title="Filter by SPU ID")
    sku_code: str | None = Field(default=None, title="Filter by SKU Code")


class SkuPageResp(PageResp):
    data: List[SkuDetail] = Field(title="SKU List")