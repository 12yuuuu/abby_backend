from fastapi import Depends
from src.core.schema import TablePageResp
from src.crud.sku_crud import SkuCrud
from src.model.models import Sku
from src.schema.sku_schema import SkuAddReq, SkuUpdateReq, SkuPageReq


class SkuService:
    def __init__(self, sku_crud: SkuCrud = Depends()) -> None:
        self._sku_crud = sku_crud

    def add_sku(self, req: SkuAddReq) -> Sku:
        sku = Sku(spu_id=req.spu_id, sku_code=req.sku_code, initial_price=req.initial_price)
        return self._sku_crud.insert_entity(sku)

    def update_sku(self, id: int, req: SkuUpdateReq) -> Sku:
        sku = self._sku_crud.select_by_id(id)
        sku.spu_id = req.spu_id
        sku.sku_code = req.sku_code
        sku.initial_price = req.initial_price
        return self._sku_crud.update_entity(sku)

    def delete_sku(self, id: int) -> None:
        self._sku_crud.delete_by_id(id)

    def get_sku_page(self, req: SkuPageReq) -> TablePageResp:
        return self._sku_crud.select_page(req, spu_id=req.spu_id, sku_code=req.sku_code)
