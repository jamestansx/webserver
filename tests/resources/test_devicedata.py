import base64
import json
import pytest
from webserver.models import User


@pytest.mark.parametrize(
    ("data", "status_code"), (({"data01": "1"}, 200), ({"data02": "1"}, 406))
)
def test_post_devicedata(test_client, login_default_user, data, status_code):
    user = login_default_user
    token = user.json["token"]
    headers = dict(Authorization=f"Bearer {token}")
    headers["content-type"] = "application/json"
    res = test_client.post(
        "/api/device/device01/data", data=json.dumps(dict(data=data)), headers=headers
    )
    print(res.json)
    assert res.status_code == status_code
