import pytest
import random
from tests.conf import *
from faker import Faker
from time import sleep


@pytest.fixture(scope="module")
def fixtures():
    faker = Faker()
    data = {
        'user_code': "".join(faker.random_letters(length=faker.random_int(min=3, max=99, step=1))),
        'user_first_name': faker.first_name(),
        'user_last_name': faker.first_name(),
        'user_email': faker.email(),
        'user_password': "".join(faker.random_letters(length=faker.random_int(min=3, max=99, step=1))),
        'user_is_enabled': faker.boolean(chance_of_getting_true=50),
        'user_timezone': faker.timezone(),
        'user_locale': random.choice(['en', 'fr']),

        'user_updated_code': "".join(faker.random_letters(length=faker.random_int(min=3, max=99, step=1))),
        'user_updated_first_name': faker.first_name(),
        'user_updated_last_name': faker.first_name(),
        'user_updated_email': faker.email(),
        'user_updated_is_enabled': faker.boolean(chance_of_getting_true=50),
        'user_updated_timezone': faker.timezone(),
        'user_updated_locale': random.choice(['en', 'fr']),
    }
    return data


def test_create_update_user(fixtures):
    user = {
        "code": fixtures["user_code"],
        "first_name": fixtures["user_first_name"],
        "last_name": fixtures["user_last_name"],
        "email": fixtures["user_email"],
        "password": fixtures["user_password"],
        "is_enabled": fixtures["user_is_enabled"],
        "timezone": fixtures["user_timezone"],
        "locale": fixtures["user_locale"],
    }
    user_created = API.user.create(user)
    assert user_created["code"] == user["code"]
    assert user_created["first_name"] == user["first_name"]
    assert user_created["last_name"] == user["last_name"]
    assert user_created["email"] == user["email"]
    assert user_created["is_enabled"] == user["is_enabled"]
    assert user_created["timezone"] == user["timezone"]
    assert user_created["locale"] == user["locale"]
    sleep(SLEEP)
    user_get = API.user.get(user_created["id"])
    assert user_get["code"] == fixtures["user_code"]

    user_update = {
        "code": fixtures["user_updated_code"],
        "first_name": fixtures["user_updated_first_name"],
        "last_name": fixtures["user_updated_last_name"],
        "email": fixtures["user_updated_email"],
        "is_enabled": fixtures["user_updated_is_enabled"],
        "timezone": fixtures["user_updated_timezone"],
        "locale": fixtures["user_updated_locale"],
    }

    user_updated = API.user.update(user_update, id=user_created["id"])
    assert user_updated["code"] == user_update["code"]
    assert user_updated["first_name"] == user_update["first_name"]
    assert user_updated["last_name"] == user_update["last_name"]
    assert user_updated["email"] == user_update["email"]
    assert user_updated["is_enabled"] == user_update["is_enabled"]
    assert user_updated["timezone"] == user_update["timezone"]
    assert user_updated["locale"] == user_update["locale"]


def test_search_users(fixtures):
    ## We sleep because the API Must reindex some results
    sleep(SLEEP)
    search_user = \
    [
        {
            "code": [
                {
                    "operator": "equals",
                    "value": {
                        "text": fixtures["user_updated_code"]
                    }
                }
            ]
        }
    ]
    user = API.user.search(search_dict=search_user)
    assert user[0]["code"] == fixtures["user_updated_code"]


def test_get_users():
    user = API.user.list(limit=1, sort="created_at:desc")
    assert len(user) == 1
    users = API.user.list(limit=2, sort="created_at:asc")
    assert len(users) == 2
    assert user[0]["code"] is not users[0]["code"]

    user_raw = API.user.list(limit=1, raw=True)
    user_recursive = API.user.list(limit=10, recursive=True)
    assert int(user_raw["total_items"]) == len(user_recursive)

    with pytest.raises(Exception):
        API.user.list(limit=1, sort="created_ats:desc")
