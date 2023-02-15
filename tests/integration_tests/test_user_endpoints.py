

def test_delete_user_success(testing_app, valid_user_id):
    response = testing_app.delete(f"/user/{valid_user_id}")
    assert response.status_code == 200


def test_delete_user_fail(testing_app, valid_user_id):
    response1 = testing_app.delete(f"/user/{valid_user_id}")
    assert response1.status_code == 200
    response2 = testing_app.delete(f"/user/{valid_user_id}")
    assert response2.status_code == 404


def test_delete_invalid_user_fail(testing_app, invalid_user_id):
    response = testing_app.delete(f"/user/{invalid_user_id}")
    assert response.status_code == 404


def test_put_user_correct_return(testing_app, sample_full_user_profile):
    user_id = 0
    response = testing_app.put(f"/user/{user_id}", json=sample_full_user_profile.dict())
    assert response.status_code == 200


