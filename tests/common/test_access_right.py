import pytest
import random
from tests.conf import *
from faker import Faker
from time import sleep
from ermeopy.schema.user_schema import type_enum


@pytest.fixture(scope="module")
def fixtures():
    faker = Faker()
    data = {
        'access_code': "".join(faker.random_letters(length=faker.random_int(min=3, max=99, step=1))),
        'access_name': faker.job(),
        'access_description': faker.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None),
        'access_type': random.choice(type_enum),
        'access_full_access': faker.boolean(chance_of_getting_true=50),
        'access_full_write': faker.boolean(chance_of_getting_true=50),
        'access_hidden': faker.boolean(chance_of_getting_true=50),

        'access_updated_code': "".join(faker.random_letters(length=faker.random_int(min=3, max=99, step=1))),
        'access_updated_name': faker.job(),
        'access_updated_description': faker.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None),
        'access_updated_type': random.choice(type_enum),
        'access_updated_full_access': faker.boolean(chance_of_getting_true=50),
        'access_updated_full_write': faker.boolean(chance_of_getting_true=50),
        'access_updated_hidden': faker.boolean(chance_of_getting_true=50),
    }
    return data


def test_create_update_access(fixtures):
    access = {
        "code": fixtures["access_code"],
        "name": fixtures["access_name"],
        "description": fixtures["access_description"],
        "type": fixtures["access_type"],
        "full_access": fixtures["access_full_access"],
        "full_write": fixtures["access_full_write"],
        "hidden": fixtures["access_hidden"],
    }
    access_created = API.user.team.access_right.create(access)
    assert access_created["code"] == access["code"]
    assert access_created["name"] == access["name"]
    assert access_created["description"] == access["description"]
    assert access_created["type"] == access["type"]
    assert access_created["full_access"] == access["full_access"]
    assert access_created["full_write"] == access["full_write"]
    assert access_created["hidden"] == access["hidden"]
    sleep(SLEEP)
    access_get = API.user.team.access_right.get(access_created["id"])
    assert access_get["code"] == fixtures["access_code"]

    access_update = {
        "code": fixtures["access_updated_code"],
        "name": fixtures["access_updated_name"],
        "description": fixtures["access_updated_description"],
        "type": fixtures["access_updated_type"],
        "full_access": fixtures["access_updated_full_access"],
        "full_write": fixtures["access_updated_full_write"],
        "hidden": fixtures["access_updated_hidden"],
    }

    access_updated = API.user.team.access_right.update(access_update, id=access_created["id"])
    assert access_updated["code"] == access_update["code"]
    assert access_updated["name"] == access_update["name"]
    assert access_updated["description"] == access_update["description"]
    assert access_updated["type"] == access_update["type"]
    assert access_updated["full_access"] == access_update["full_access"]
    assert access_updated["full_write"] == access_update["full_write"]
    assert access_updated["hidden"] == access_update["hidden"]

    API.user.team.access_right.delete(access_created["id"])
    with pytest.raises(Exception):
        API.user.team.access_right.get(access_created["id"])

    access_recreated = API.user.team.access_right.create(access_update)
    assert access_recreated["code"] == fixtures["access_updated_code"]


def test_search_access(fixtures):
    sleep(SLEEP)
    search_access = \
    [
        {
            "code": [
                {
                    "operator": "equals",
                    "value": {
                        "text": fixtures["access_updated_code"]
                    }
                }
            ]
        }
    ]
    with pytest.raises(Exception):
        API.user.team.access_right.search(search_dict=search_access)


def test_get_accesses():
    access = API.user.team.access_right.list(limit=1, sort="created_at:desc")
    assert len(access) == 1
    accesses = API.user.team.access_right.list(limit=2, sort="created_at:asc")
    assert len(accesses) == 2
    assert access[0]["code"] is not accesses[0]["code"]

    access_raw = API.user.team.access_right.list(limit=1, raw=True)
    access_recursive = API.user.team.access_right.list(limit=10, recursive=True)
    assert int(access_raw["total_items"]) == len(access_recursive)

    with pytest.raises(Exception):
        API.user.list(limit=1, sort="created_ats:desc")
