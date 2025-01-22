from sqlmodel import SQLModel, Field, String, Integer, Float, BigInteger, Boolean, Relationship
from typing import Optional, List
from src.core.database import BaseTable

class Product(BaseTable, table=True):
    __tablename__ = "product"

    name: str = Field(sa_column_kwargs={"comment": "Product name"})
    category: str = Field(sa_column_kwargs={"comment": "Product category"})
    price: float = Field(sa_column_kwargs={"comment": "Product price"})

    transactions: List["Transaction"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class Transaction(BaseTable, table=True):
    __tablename__ = "transaction"

    product_id: int = Field(foreign_key="product.id", sa_column_kwargs={"comment": "Product ID"})
    customer_id: int = Field(foreign_key="customer.id", sa_column_kwargs={"comment": "Customer ID"})
    date: int = Field(sa_type=BigInteger, sa_column_kwargs={"comment": "Transaction date (timestamp)"})
    quantity: int = Field(sa_column_kwargs={"comment": "Quantity sold"})

    product: Optional["Product"] = Relationship(back_populates="transactions")
    customer: Optional["Customer"] = Relationship(back_populates="transactions")

class Customer(BaseTable, table=True):
    __tablename__ = "customer"

    name: str = Field(sa_column_kwargs={"comment": "Customer name"})
    age: int = Field(sa_column_kwargs={"comment": "Customer age"})
    gender: str = Field(sa_column_kwargs={"comment": "Customer gender"}) 

    transactions: List[Transaction] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class ChatMessage(BaseTable, table=True):
    __tablename__ = "chat_message"

    chat_id: int = Field(index=True, sa_column_kwargs={"comment": "Chat ID"})
    role: str = Field(sa_column_kwargs={"comment": "Role (user or abby)"})  # user or abby
    message_type: str = Field(sa_column_kwargs={"comment": "Message type (text or image)"})  # text or image
    message_data: str = Field(sa_column_kwargs={"comment": "Message data (text content or file URL)"})

