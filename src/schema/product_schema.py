from pydantic import BaseModel, Field
from typing import List
from src.core.schema import PageReq, PageResp


class ProductAddReq(BaseModel):
    name: str = Field(title="Product Name")
    category: str = Field(title="Product Category")
    price: float = Field(title="Product Price", ge=0)


class ProductUpdateReq(ProductAddReq):
    pass


class ProductDetail(BaseModel):
    id: int = Field(title="Product ID")
    name: str = Field(title="Product Name")
    category: str = Field(title="Product Category")
    price: float = Field(title="Product Price")
    

class ProductPageReq(PageReq):
    name: str | None = Field(default=None, title="Filter by Name")
    category: str | None = Field(default=None, title="Filter by Category")


class ProductPageResp(PageResp):
    data: List[ProductDetail] = Field(title="Product List")
