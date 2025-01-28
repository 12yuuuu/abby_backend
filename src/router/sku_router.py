from fastapi import APIRouter, Query, Path, Body, Depends
from src.core.schema import SuccessResp
from src.schema.sku_schema import (
    SkuAddReq,
    SkuUpdateReq,
    SkuDetail,
    SkuPageReq,
    SkuPageResp,
)
from src.service.sku_service import SkuService

router = APIRouter(prefix="/sku", tags=["SKU Management"])


@router.get("", summary="Get SKU list", response_model=SkuPageResp)
def get_sku_page(
    req: SkuPageReq = Query(),
    service: SkuService = Depends(),
):
    return service.get_sku_page(req)


@router.post("", summary="Add SKU", response_model=SkuDetail)
def add_sku(req: SkuAddReq, service: SkuService = Depends()):
    return service.add_sku(req)


@router.put("/{id}", summary="Update SKU", response_model=SkuDetail)
def update_sku(
    id: int = Path(), req: SkuUpdateReq = Body(), service: SkuService = Depends()
):
    return service.update_sku(id, req)


@router.delete("/{id}", summary="Delete SKU", response_model=SuccessResp)
def delete_sku(id: int = Path(), service: SkuService = Depends()):
    service.delete_sku(id)
    return SuccessResp()