from fastapi import Depends
from src.core.schema import TablePageResp
from src.crud.transaction_crud import TransactionCrud
from src.model.models import Transaction
from src.schema.transaction_schema import (
    TransactionAddReq,
    TransactionUpdateReq,
    TransactionPageReq,
)


class TransactionService:
    def __init__(self, transaction_crud: TransactionCrud = Depends()) -> None:
        self._transaction_crud = transaction_crud

    def add_transaction(self, req: TransactionAddReq) -> Transaction:
        transaction = Transaction(
            product_id=req.product_id,
            customer_id=req.customer_id,
            date=req.date,
            quantity=req.quantity,
        )
        return self._transaction_crud.insert_entity(transaction)

    def update_transaction(self, id: int, req: TransactionUpdateReq) -> Transaction:
        transaction = self._transaction_crud.select_by_id(id)
        transaction.product_id = req.product_id
        transaction.customer_id = req.customer_id
        transaction.date = req.date
        transaction.quantity = req.quantity
        return self._transaction_crud.update_entity(transaction)

    def delete_transaction(self, id: int) -> None:
        self._transaction_crud.delete_by_id(id)

    def get_transaction_page(self, req: TransactionPageReq) -> TablePageResp:
        return self._transaction_crud.select_page(
            req,
            product_id=req.product_id,
            customer_id=req.customer_id,
            date_range=req.date_range,
        )
