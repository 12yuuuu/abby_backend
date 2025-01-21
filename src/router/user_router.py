from fastapi import APIRouter, Body, Depends, Path, Query

from src.core.dependency import get_ip, get_login_user
from src.core.schema import LoginUser, SuccessResp
from src.schema.user_schema import (
    UserAddReq,
    UserDetail,
    UserPageReq,
    UserPageResp,
    UserUpdateReq,
)
from src.service.user_service import UserService


router = APIRouter(prefix="/path", tags=["User Management"])


@router.get("", summary="Get user list", response_model=UserPageResp)
def get_page(
    req: UserPageReq = Query(),
    service: UserService = Depends(),
):

    return service.get_user_page(req)


@router.post("", summary="Add user", response_model=UserDetail)
def add_user(req: UserAddReq, service: UserService = Depends()):
    return service.add_user(req)


@router.put("/{id}", summary="Update user", response_model=UserDetail)
def update_user(
    id: int = Path(), req: UserUpdateReq = Body(), service: UserService = Depends()
):
    return service.update_user(id, req)


@router.delete("/{id}", summary="Delete user", response_model=SuccessResp)
def delete_user(id: int = Path(), service: UserService = Depends()):
    service.delete_user(id)
    return SuccessResp()
