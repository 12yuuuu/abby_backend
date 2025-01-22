from fastapi import APIRouter, Path, Query, Body, Depends
from src.schema.customer_schema import CustomerAddReq, CustomerUpdateReq, CustomerDetail, CustomerPageReq, CustomerPageResp
from src.service.customer_service import CustomerService
from src.core.schema import SuccessResp

router = APIRouter(prefix="/customer", tags=["Customer Management"])


@router.get("", summary="Get customer list", response_model=CustomerPageResp)
def get_customer_page(
    req: CustomerPageReq = Query(),
    service: CustomerService = Depends(),
):
    return service.get_customer_page(req)


@router.post("", summary="Add customer", response_model=CustomerDetail)
def add_customer(req: CustomerAddReq, service: CustomerService = Depends()):
    return service.add_customer(req)


@router.put("/{id}", summary="Update customer", response_model=CustomerDetail)
def update_customer(
    id: int = Path(), req: CustomerUpdateReq = Body(), service: CustomerService = Depends()
):
    return service.update_customer(id, req)


@router.delete("/{id}", summary="Delete customer", response_model=SuccessResp)
def delete_customer(id: int = Path(), service: CustomerService = Depends()):
    service.delete_customer(id)
    return SuccessResp()
