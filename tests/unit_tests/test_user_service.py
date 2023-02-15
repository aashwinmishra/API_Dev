import pytest


@pytest.mark.asyncio
async def test_delete_user(user_service, valid_user_id):
    await user_service.delete_user(valid_user_id)
    assert valid_user_id not in user_service.profile_infos
    assert valid_user_id not in user_service.user_contents

