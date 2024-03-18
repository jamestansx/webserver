def test_home_page_nologin(test_client):
    res = test_client.get("/")

    assert res.status_code == 200
    assert b"register" in res.data


def test_home_page_login(test_client, login_default_user_form, new_user):

    assert login_default_user_form.status_code == 200
    assert new_user.username.encode() in login_default_user_form.data
