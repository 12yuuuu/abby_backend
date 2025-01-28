from fastapi import APIRouter, Query, Path, Body, Depends
from src.core.schema import SuccessResp
from src.schema.spu_schema import (
    SpuAddReq,
    SpuUpdateReq,
    SpuDetail,
    SpuPageReq,
    SpuPageResp,
)
from src.service.spu_service import SpuService

router = APIRouter(prefix="/spu", tags=["SPU Management"])


@router.get("", summary="Get SPU list", response_model=SpuPageResp)
def get_spu_page(
    req: SpuPageReq = Query(),
    service: SpuService = Depends(),
):
    return service.get_spu_page(req)


@router.post("", summary="Add SPU", response_model=SpuDetail)
def add_spu(req: SpuAddReq, service: SpuService = Depends()):
    return service.add_spu(req)


@router.put("/{id}", summary="Update SPU", response_model=SpuDetail)
def update_spu(
    id: int = Path(), req: SpuUpdateReq = Body(), service: SpuService = Depends()
):
    return service.update_spu(id, req)


@router.delete("/{id}", summary="Delete SPU", response_model=SuccessResp)
def delete_spu(id: int = Path(), service: SpuService = Depends()):
    service.delete_spu(id)
    return SuccessResp()