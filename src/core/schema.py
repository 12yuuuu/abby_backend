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


# 新增針對交易、產品和客戶的 Schema
class Product(BaseModel):
    """Product schema"""

    id: int = Field(title="Product ID")
    name: str = Field(title="Product Name")
    category: str = Field(title="Product Category")
    price: float = Field(title="Product Price")
    cost: float = Field(title="Product Cost")


class Customer(BaseModel):
    """Customer schema"""

    id: int = Field(title="Customer ID")
    name: str = Field(title="Customer Name")
    age: int = Field(title="Customer Age")
    gender: str = Field(title="Customer Gender")
    location: str = Field(title="Customer Location")


class Transaction(BaseModel):
    """Transaction schema"""

    id: int = Field(title="Transaction ID")
    product_id: int = Field(title="Product ID")
    customer_id: int = Field(title="Customer ID")
    date: int = Field(title="Transaction Date (timestamp)")
    quantity: int = Field(title="Quantity Sold")


# 針對查詢數據的響應 Schema
class ProductSalesTrendResp(BaseModel):
    """Product sales trend response"""

    date: str = Field(title="Date")
    sales: float = Field(title="Sales Amount")


class CustomerPurchaseResp(BaseModel):
    """Customer purchase data response"""

    customer: Customer
    transactions: List[Transaction]


class ProductPerformanceResp(BaseModel):
    """Product performance data response"""

    product: Product
    total_quantity: int
