from fastapi import Depends
from src.core.schema import TablePageResp
from src.crud.product_crud import ProductCrud
from src.model.models import Product
from src.schema.product_schema import ProductAddReq, ProductUpdateReq, ProductPageReq


class ProductService:
    def __init__(self, product_crud: ProductCrud = Depends()) -> None:
        self._product_crud = product_crud

    def add_product(self, req: ProductAddReq) -> Product:
        product = Product(name=req.name, category=req.category, price=req.price)
        return self._product_crud.insert_entity(product)

    def update_product(self, id: int, req: ProductUpdateReq) -> Product:
        product = self._product_crud.select_by_id(id)
        product.name = req.name
        product.category = req.category
        product.price = req.price
        return self._product_crud.update_entity(product)

    def delete_product(self, id: int) -> None:
        self._product_crud.delete_by_id(id)

    def get_product_page(self, req: ProductPageReq) -> TablePageResp:
        return self._product_crud.select_page(req, name=req.name, category=req.category)
