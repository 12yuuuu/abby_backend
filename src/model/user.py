from sqlmodel import Field, String, Integer
from src.core.database import BaseTable


class User(BaseTable, table=True):
    __tablename__ = "user_demo"
    username: str = Field(sa_type=String(32), sa_column_kwargs={"comment": "用户名"})
    age: int = Field(
        sa_type=Integer, sa_column_kwargs={"comment": "年龄"}, ge=0, le=200
    )
