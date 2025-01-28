from fastapi import APIRouter, Query, Path, Body, Depends
from src.core.schema import SuccessResp
from src.schema.transaction_schema import (
    TransactionAddReq,
    TransactionUpdateReq,
    TransactionDetail,
    TransactionPageReq,
    TransactionPageResp,
)
from src.service.transaction_service import TransactionService

router = APIRouter(prefix="/transaction", tags=["Transaction Management"])


@router.get("", summary="Get transaction list", response_model=TransactionPageResp)
def get_transaction_page(
    req: TransactionPageReq = Query(),
    service: TransactionService = Depends(),
):
    return service.get_transaction_page(req)


@router.post("", summary="Add transaction", response_model=TransactionDetail)
def add_transaction(req: TransactionAddReq, service: TransactionService = Depends()):
    return service.add_transaction(req)


@router.put("/{id}", summary="Update transaction", response_model=TransactionDetail)
def update_transaction(
    id: int = Path(), req: TransactionUpdateReq = Body(), service: TransactionService = Depends()
):
    return service.update_transaction(id, req)


@router.delete("/{id}", summary="Delete transaction", response_model=SuccessResp)
def delete_transaction(id: int = Path(), service: TransactionService = Depends()):
    service.delete_transaction(id)
    return SuccessResp()
