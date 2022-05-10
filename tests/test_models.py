import pytest
from webserver.models import User, DeviceInfo, DataType, Data


def test_new_user(new_user):

    assert new_user.username == "user01"
    with pytest.raises(AttributeError):
        new_user.password


def test_new_device(new_device, new_datatype):

    assert new_device.name == "device01"
    assert new_device.datatype == [new_datatype]


def test_new_datatype(new_datatype):

    assert new_datatype.name == "data01"
