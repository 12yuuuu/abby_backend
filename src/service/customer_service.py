from fastapi import Depends
from src.core.schema import TablePageResp
from src.crud.customer_crud import CustomerCrud
from src.model.models import Customer
from src.schema.customer_schema import CustomerAddReq, CustomerUpdateReq, CustomerPageReq


class CustomerService:
    def __init__(self, customer_crud: CustomerCrud = Depends()) -> None:
        self._customer_crud = customer_crud

    def add_customer(self, req: CustomerAddReq) -> Customer:
        customer = Customer(name=req.name, age=req.age, gender=req.gender)
        return self._customer_crud.insert_entity(customer)

    def update_customer(self, id: int, req: CustomerUpdateReq) -> Customer:
        customer = self._customer_crud.select_by_id(id)
        customer.name = req.name
        customer.age = req.age
        customer.gender = req.gender
        return self._customer_crud.update_entity(customer)

    def delete_customer(self, id: int) -> None:
        self._customer_crud.delete_by_id(id)

    def get_customer_page(self, req: CustomerPageReq) -> TablePageResp:
        return self._customer_crud.select_page(req, name=req.name, gender=req.gender, age=req.age)
