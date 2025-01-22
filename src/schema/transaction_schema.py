from pydantic import BaseModel, Field
from typing import Optional, List, Tuple
from src.core.schema import PageReq, PageResp


class TransactionAddReq(BaseModel):
    product_id: int = Field(title="Product ID")
    customer_id: int = Field(title="Customer ID")
    date: int = Field(title="Transaction Date (timestamp)")
    quantity: int = Field(title="Quantity Sold", ge=1)


class TransactionUpdateReq(TransactionAddReq):
    pass


class TransactionDetail(BaseModel):
    id: int = Field(title="Transaction ID")
    product_id: int = Field(title="Product ID")
    customer_id: int = Field(title="Customer ID")
    date: int = Field(title="Transaction Date (timestamp)")
    quantity: int = Field(title="Quantity Sold")


class TransactionPageReq(PageReq):
    product_id: Optional[int] = Field(default=None, title="Filter by Product ID")
    customer_id: Optional[int] = Field(default=None, title="Filter by Customer ID")
    date_range: Optional[Tuple[int, int]] = Field(
        default=None, title="Filter by Date Range", description="Provide a tuple (start_date, end_date)"
    )


class TransactionPageResp(PageResp):
    data: List[TransactionDetail] = Field(title="List of Transactions")
