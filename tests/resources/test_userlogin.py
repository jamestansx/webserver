import base64
import pytest
from webserver.models import User


@pytest.mark.parametrize(
    ("username", "password", "status_code"),
    (("", "", 401), ("a", "b", 401), ("user01", "1234", 200)),
)
def test_login_validate_input(test_client, init_db, username, password, status_code):

    auth = f"{username}:{password}"
    headers = dict(Authorization=f"Basic {base64.b64encode(auth.encode()).decode()}")

    res = test_client.get("/api/user/login", headers=headers)

    print(res.text)
    assert res.status_code == status_code
