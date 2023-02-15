import pytest
from app.schemas.user import FullUserProfile


@pytest.fixture
def valid_user_id() -> int:
    return 0


@pytest.fixture
def invalid_user_id() -> int:
    return 99999


@pytest.fixture
def sample_full_user_profile() -> FullUserProfile:
    return FullUserProfile(username='Sample User',
                           liked_posts=[1, 2],
                           short_description="SampleUser",
                           long_bio="Sample User")
