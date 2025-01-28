from fastapi import Depends
from src.core.schema import TablePageResp
from src.crud.client_crud import ClientCrud
from src.model.models import Client
from src.schema.client_schema import ClientAddReq, ClientUpdateReq, ClientPageReq


class ClientService:
    def __init__(self, client_crud: ClientCrud = Depends()) -> None:
        self._client_crud = client_crud

    def add_client(self, req: ClientAddReq) -> Client:
        client = Client(
            tenant_id=req.tenant_id,
            openid=req.openid,
            follow_source=req.follow_source,
            name=req.name,
            age=req.age,
            gender=req.gender,
            email=req.email,
            tel=req.tel,
            address=req.address,
            contact=req.contact,
            qq=req.qq,
            weibo=req.weibo,
            weixin=req.weixin,
            comment=req.comment,
        )
        return self._client_crud.insert_entity(client)

    def update_client(self, id: int, req: ClientUpdateReq) -> Client:
        client = self._client_crud.select_by_id(id)
        # Only update fields if they are provided
        if req.name is not None:
            client.name = req.name
        if req.gender is not None:
            client.gender = req.gender
        if req.age is not None:
            client.age = req.age
        if req.email is not None:
            client.email = req.email
        if req.tel is not None:
            client.tel = req.tel
        if req.address is not None:
            client.address = req.address
        if req.contact is not None:
            client.contact = req.contact
        if req.qq is not None:
            client.qq = req.qq
        if req.weibo is not None:
            client.weibo = req.weibo
        if req.weixin is not None:
            client.weixin = req.weixin
        if req.comment is not None:
            client.comment = req.comment
        return self._client_crud.update_entity(client)

    def delete_client(self, id: int) -> None:
        self._client_crud.delete_by_id(id)

    def get_client_page(self, req: ClientPageReq) -> TablePageResp:
        return self._client_crud.select_page(
            req,
            tenant_id=req.tenant_id,
            name=req.name,
            gender=req.gender,
            age=req.age
        )
