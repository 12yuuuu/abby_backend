from fastapi import Depends
from datetime import datetime
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
            client_id=req.client_id,
            sku_id=req.sku_id,
            quantity=req.quantity,
            amount=req.amount,
            currency=req.currency,
            transaction_date=req.transaction_date,
        )
        return self._transaction_crud.insert_entity(transaction)

    def update_transaction(self, id: int, req: TransactionUpdateReq) -> Transaction:
        transaction = self._transaction_crud.select_by_id(id)
        transaction.client_id = req.client_id
        transaction.sku_id = req.sku_id
        transaction.quantity = req.quantity
        transaction.amount = req.amount
        transaction.currency = req.currency
        transaction.transaction_date = req.transaction_date
        return self._transaction_crud.update_entity(transaction)

    def get_transaction_page(self, req: TransactionPageReq) -> TablePageResp:
        return self._transaction_crud.select_page(
            req,
            client_id=req.client_id,
            sku_id=req.sku_id,
            date_range=req.date_range,  # Pass datetime range directly
        )

    def delete_transaction(self, id: int) -> None:
        self._transaction_crud.delete_by_id(id)