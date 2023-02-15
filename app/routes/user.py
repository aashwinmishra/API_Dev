from fastapi import APIRouter, HTTPException, Response, Depends
from app.schemas.user import FullUserProfile, MultipleUsersResponse, CreateUserResponse
from app.services.user import UserService
import logging
from app.clients.db import DatabaseClient


logger = logging.getLogger(__name__)


def create_user_router(database_client: DatabaseClient) -> APIRouter:
    user_router = APIRouter(prefix="/user", tags=["user"])
    user_service = UserService(database_client)

    @user_router.get("/all", response_model=MultipleUsersResponse)
    async def get_all_users_paginated(start: int = 0, limit: int = 2):
        l = await user_service.get_all_users_with_pagination(start, limit)
        return MultipleUsersResponse(users=l)

    @user_router.get("/{user_id}", response_model=FullUserProfile)
    async def get_user_by_id(user_id: int):
        full_user_profile = await user_service.get_user_info(user_id)
        return full_user_profile

    @user_router.put("/{user_id}")
    async def update_user(user_id: int, full_profile_info: FullUserProfile):
        new_user_id = await user_service.create_update_user(full_profile_info, user_id)
        return new_user_id

    @user_router.delete("/{user_id}")
    async def remove_user(user_id: int):
        try:
            await user_service.delete_user(user_id)
        except KeyError:
            logger.error("Non-existent User ID requested")
            raise HTTPException(status_code=404, detail="User Not Found")

    @user_router.post("/", response_model=CreateUserResponse, status_code=201)
    async def add_user(full_profile_info: FullUserProfile):
        new_user_id = await user_service.create_update_user(full_profile_info)
        return CreateUserResponse(user_id=new_user_id)

    # @user_router.get("/test", response_class=JSONResponse)
    # def test():
    #     return {"Python Version:": platform.python_version()}

    return user_router
