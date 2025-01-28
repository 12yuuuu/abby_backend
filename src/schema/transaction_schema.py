from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Tuple
from src.core.schema import PageReq, PageResp


class TransactionAddReq(BaseModel):
    client_id: int = Field(title="Client ID")
    sku_id: int = Field(title="SKU ID")
    quantity: int = Field(title="Quantity", ge=1)
    amount: float = Field(title="Total Amount")
    currency: str = Field(title="Currency")
    transaction_date: datetime = Field(title="Transaction Date (datetime)")


class TransactionUpdateReq(TransactionAddReq):
    pass


class TransactionDetail(BaseModel):
    id: int = Field(title="Transaction ID")
    tenant_id: str = Field(title="Tenant ID")
    client_id: int = Field(title="Client ID")
    sku_id: int = Field(title="SKU ID")
    quantity: int = Field(title="Quantity")
    amount: float = Field(title="Total Amount")
    currency: str = Field(title="Currency")
    transaction_date: datetime = Field(title="Transaction Date")
    payment_method: Optional[str] = Field(title="Payment Method")
    shipping_status: Optional[str] = Field(title="Shipping Status")
    discount: float = Field(title="Discount")
    promotion_id: Optional[str] = Field(title="Promotion ID")
    comment: Optional[str] = Field(title="Comment")


class TransactionPageReq(PageReq):
    client_id: Optional[int] = Field(default=None, title="Filter by Client ID")
    sku_id: Optional[int] = Field(default=None, title="Filter by SKU ID")
    date_range: Optional[Tuple[datetime, datetime]] = Field(
        default=None, title="Filter by Date Range", description="Provide a tuple (start_date, end_date)"
    )


class TransactionPageResp(PageResp):
    data: List[TransactionDetail] = Field(title="List of Transactions")

