from fastapi import Depends
from src.core.schema import TablePageResp
from src.crud.user_crud import UserCrud
from src.model.user import User
from src.schema.user_schema import UserAddReq, UserPageReq, UserUpdateReq


class UserService:
    def __init__(self, user_crud: UserCrud = Depends()) -> None:
        self._user_crud = user_crud

    def add_user(self, req: UserAddReq) -> User:
        user = User(username=req.username, age=req.age)
        return self._user_crud.insert_entity(user)

    def update_user(self, id: int, req: UserUpdateReq) -> User:
        user = self._user_crud.select_by_id(id)
        user.username = req.username
        user.age = req.age
        return self._user_crud.update_entity(user)

    def delete_user(self, id: int) -> None:
        self._user_crud.delete_by_id(id)

    def get_user_page(self, req: UserPageReq) -> TablePageResp:
        return self._user_crud.select_page(req, username=req.username, age=req.age)
