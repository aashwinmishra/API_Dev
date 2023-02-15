from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field(default="Unnamed User",
                          alias="name",
                          title="Name",
                          description="User Name",
                          min_length=1, max_length=25)
    liked_posts: list[int] = Field(default=None, min_items=1, max_items=10)


class FullUserProfile(User):
    short_description: str
    long_bio: str


class MultipleUsersResponse(BaseModel):
    users: list[FullUserProfile]


class CreateUserResponse(BaseModel):
    user_id: int = None

