from fastapi import APIRouter, Path, Query, Body, Depends
from src.schema.product_schema import ProductAddReq, ProductUpdateReq, ProductDetail, ProductPageReq, ProductPageResp
from src.service.product_service import ProductService
from src.core.schema import SuccessResp

router = APIRouter(prefix="/product", tags=["Product Management"])


@router.get("", summary="Get product list", response_model=ProductPageResp)
def get_product_page(
    req: ProductPageReq = Query(),
    service: ProductService = Depends(),
):
    return service.get_product_page(req)


@router.post("", summary="Add product", response_model=ProductDetail)
def add_product(req: ProductAddReq, service: ProductService = Depends()):
    return service.add_product(req)


@router.put("/{id}", summary="Update product", response_model=ProductDetail)
def update_product(
    id: int = Path(), req: ProductUpdateReq = Body(), service: ProductService = Depends()
):
    return service.update_product(id, req)


@router.delete("/{id}", summary="Delete product", response_model=SuccessResp)
def delete_product(id: int = Path(), service: ProductService = Depends()):
    service.delete_product(id)
    return SuccessResp()
