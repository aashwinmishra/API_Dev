import pytest
from app.services.user import UserService


@pytest.fixture
def _profile_infos():
    profile_infos = {0: {"short_description": "Short Desc", "long_bio": "Long Biography"},
                         1: {"short_description": "Short Desc", "long_bio": "Long Biography"},
                         2: {"short_description": "Short Desc", "long_bio": "Long Biography"},
                         3: {"short_description": "Short Desc", "long_bio": "Long Biography"},
                         4: {"short_description": "Short Desc", "long_bio": "Long Biography"}
                         }

    return profile_infos


@pytest.fixture
def _user_contents():
    user_contents = {0: {"username": "User 0", "liked_posts": [1, 2]},
                         1: {"username": "User 1", "liked_posts": [1, 2, 3]},
                         2: {"username": "User 2", "liked_posts": [1, 2, 3, 4]},
                         3: {"username": "User 3", "liked_posts": [1, 2, 3]},
                         4: {"username": "User 4", "liked_posts": [1, 2, 3, 4]}
                         }
    return user_contents


@pytest.fixture
def user_service(_profile_infos, _user_contents):
    user_service = UserService(_profile_infos, _user_contents)
    return user_service