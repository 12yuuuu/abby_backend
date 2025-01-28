from fastapi import Depends
from src.core.schema import TablePageResp
from src.crud.spu_crud import SpuCrud
from src.model.models import Spu
from src.schema.spu_schema import SpuAddReq, SpuUpdateReq, SpuPageReq


class SpuService:
    def __init__(self, spu_crud: SpuCrud = Depends()) -> None:
        self._spu_crud = spu_crud

    def add_spu(self, req: SpuAddReq) -> Spu:
        spu = Spu(title=req.title, brand=req.brand)
        return self._spu_crud.insert_entity(spu)

    def update_spu(self, id: int, req: SpuUpdateReq) -> Spu:
        spu = self._spu_crud.select_by_id(id)
        spu.title = req.title
        spu.brand = req.brand
        return self._spu_crud.update_entity(spu)

    def delete_spu(self, id: int) -> None:
        self._spu_crud.delete_by_id(id)

    def get_spu_page(self, req: SpuPageReq) -> TablePageResp:
        return self._spu_crud.select_page(req, title=req.title, brand=req.brand)