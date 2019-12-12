import pytest
from tests.conf import *
from faker import Faker
from time import sleep


@pytest.fixture(scope="module")
def fixtures():
    faker = Faker()
    data = {
        'role_code': "".join(faker.random_letters(length=faker.random_int(min=3, max=99, step=1))),
        'role_name': faker.job(),
        'role_enabled': faker.boolean(chance_of_getting_true=50),
        'role_platform_permission': [x for x in range(1, 40)],
        'role_app_permission': [x for x in range(1001, 1020)],

        'role_updated_code': "".join(faker.random_letters(length=faker.random_int(min=3, max=99, step=1))),
        'role_updated_name': faker.job(),
        'role_updated_enabled': faker.boolean(chance_of_getting_true=50),
    }
    return data


def test_create_update_role(fixtures):
    role = {
        "code": fixtures["role_code"],
        "name": fixtures["role_name"],
        "enabled": fixtures["role_enabled"],
        "platform_permission": fixtures["role_platform_permission"],
        "app_permission": fixtures["role_app_permission"],
    }
    role_created = API.user.role.create(role)
    assert role_created["code"] == role["code"]
    assert role_created["name"] == role["name"]
    assert role_created["enabled"] == role["enabled"]
    assert len(role_created["platform_permission"]) == len(role["platform_permission"])
    assert len(role_created["app_permission"]) == len(role["app_permission"])

    sleep(SLEEP)
    role_get = API.user.role.get(role_created["id"])
    assert role_get["code"] == fixtures["role_code"]

    role_update = {
        "code": fixtures["role_updated_code"],
        "name": fixtures["role_updated_name"],
        "enabled": fixtures["role_updated_enabled"],
    }

    role_updated = API.user.role.update(role_update, id=role_created["id"], admin=True)
    assert role_updated["code"] == role_update["code"]
    assert role_updated["name"] == role_update["name"]
    assert role_updated["enabled"] == role_update["enabled"]
    assert len(role_updated["platform_permission"]) == len(role_update["platform_permission"])
    assert len(role_updated["app_permission"]) == len(role_update["app_permission"])


def test_get_roles():
    role = API.user.role.list(limit=1, sort="created_at:desc")
    assert len(role) == 1
    roles = API.user.role.list(limit=2, sort="created_at:asc")
    assert len(roles) == 2
    assert role[0]["code"] is not roles[0]["code"]

    role_raw = API.user.role.list(limit=1, raw=True)
    role_recursive = API.user.role.list(limit=10, recursive=True)
    assert int(role_raw["total_items"]) == len(role_recursive)

    with pytest.raises(Exception):
        API.user.role.list(limit=1, sort="created_ats:desc")
