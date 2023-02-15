from typing import Optional, Tuple
from app.schemas.user import (
    FullUserProfile,
    User,
)
from app.clients.db import DatabaseClient
from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import Select


class UserService:

    def __init__(self, database_client: DatabaseClient):
        self.database_client = database_client

    async def get_all_users_with_pagination(self, offset: int, limit: int) -> Tuple[list[FullUserProfile], int]:
        query = self._get_user_info_query()
        users = self.database_client.get_paginated(query, limit, offset)

        total_query = select(func.count(self.database_client.user.c.id).label("total"))
        total = self.database_client.get_first(total_query)[0]
        user_infos = []
        for user in users:
            user_info = dict(zip(user.keys(), user))
            full_user_profile = FullUserProfile(**user_info)
            user_infos.append(full_user_profile)

        return user_infos, total

    async def get_user_info(self, user_id: int = 0) -> FullUserProfile:
        query = self._get_user_info_query(user_id)
        user = self.database_client.get_first(query)

        user_info = dict(zip(user.keys(), user))

        return FullUserProfile(**user_info)

    async def create_update_user(self, full_profile_info: FullUserProfile, user_id: Optional[int] = None) -> int:
        if user_id is None:
            user_id = len(self.profile_infos)
        liked_posts = full_profile_info.liked_posts
        short_description = full_profile_info.short_description
        long_bio = full_profile_info.long_bio

        self.users_content[user_id] = {"liked_posts": liked_posts}
        self.profile_infos[user_id] = {
            "short_description": short_description,
            "long_bio": long_bio
        }

        return user_id

    async def delete_user(self, user_id: int) -> None:

        del self.profile_infos[user_id]
        del self.users_content[user_id]

    def _get_user_info_query(self, user_id: Optional[int] = None) -> Select:
        liked_posts_query = (
            select(
                self.database_client.liked_post.c.user_id,
                func.array_agg(self.database_client.liked_post.c.post_id).label("liked_posts")
        )
            .group_by(self.database_client.liked_post.c.user_id)
        )
        if user_id:
            liked_posts_query = liked_posts_query.where(self.database_client.liked_post.c.user_id == user_id)
        liked_posts_query = liked_posts_query.cte("liked_posts_query")

        query = (
            select(
                self.database_client.user.c.short_description,
                self.database_client.user.c.long_bio,
                self.database_client.user.c.username.label("name"),
                liked_posts_query.c.liked_posts
            )
            .join(
                liked_posts_query,
                liked_posts_query.c.user_id == self.database_client.user.c.id,
                isouter=True
            )
        )
        if user_id:
            query = query.where(self.database_client.user.c.id == user_id)

        return query

