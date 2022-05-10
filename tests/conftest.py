import base64
import os
import pytest
from webserver import create_app, db
from webserver.models import User, DeviceInfo, DataType, Data
from webserver.forms import UserLoginForm

BASEDIR = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope="module")
def test_client():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///"
            + os.path.join(BASEDIR, "webserver_test.db"),
            "PRESERVE_CONTEXT_ON_EXCEPTION": False,
        }
    )

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def init_db(test_client, new_user):
    db.create_all()

    db.session.add(new_user)
    db.session.commit()

    yield

    db.drop_all()


@pytest.fixture(scope="module")
def new_user(new_device):
    user = User(username="user01", password="1234")
    user.devicelist.append(
        DeviceInfo(name="device01", datatype=[DataType(name="data01")])
    )
    return user


@pytest.fixture(scope="module")
def new_device(new_datatype):
    return DeviceInfo(name="device01", datatype=[new_datatype])


@pytest.fixture(scope="module")
def new_datatype():
    return DataType(name="data01")


@pytest.fixture(scope="module")
def login_default_user(test_client, init_db):
    auth = f"user01:1234"
    headers = dict(Authorization=f"Basic {base64.b64encode(auth.encode()).decode()}")
    res = test_client.get("/api/user/login", headers=headers)
    return res


@pytest.fixture(scope="module")
def login_default_user_form(test_client, init_db, new_user):
    res = test_client.post(
        "/users/login",
        data=dict(username="user01", password="1234"),
        follow_redirects=True,
    )
    return res
