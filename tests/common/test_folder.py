import pytest
from tests.conf import *
from faker import Faker
from time import sleep


@pytest.fixture(scope="module")
def fixtures():
    faker = Faker()
    data = {
        'folder_parent_name': "".join(faker.random_letters(length=faker.random_int(min=0, max=99, step=1))),
        'folder_children_name': "".join(faker.random_letters(length=faker.random_int(min=0, max=99, step=1))),
    }
    return data


def test_create_folder(fixtures):
    folder_parent = {
        "name": fixtures["folder_parent_name"],
        "resource": {"type": "document"}
    }

    folder_parent_created = API.folder.create(folder_parent)
    assert folder_parent_created["name"] == folder_parent["name"]
    assert folder_parent_created["parent"] is None
    assert folder_parent_created["has_children"] == False

    folder_children = {
        "name": fixtures["folder_children_name"],
        "parent": {"id": folder_parent_created["id"]},
        "resource": {"type": "document"}
    }

    folder_children_api = API.folder.create(folder_children)
    assert folder_children_api["parent"]["id"] == folder_parent_created["id"]
    assert folder_children_api["has_children"] == False


def test_search_folders(fixtures):
    ## We sleep because the API Must reindex some results
    sleep(SLEEP)
    search_children_folder = \
    [
        {
            "name": [
                {
                    "operator": "contains",
                    "value": {
                        "text": fixtures["folder_children_name"]
                    }
                }
            ]
        }
    ]
    children_folder = API.folder.search(search_dict=search_children_folder)
    assert children_folder[0]["name"] == fixtures["folder_children_name"]
    search_parent_folder = \
        [
            {
                "name": [
                    {
                        "operator": "contains",
                        "value": {
                            "text": fixtures["folder_parent_name"]
                        }
                    }
                ]
            }
        ]
    parent_folder = API.folder.search(search_dict=search_parent_folder)
    assert parent_folder[0]["name"] == fixtures["folder_parent_name"]


def test_get_folders():
    folders_1 = API.folder.get(limit=1, sort="created_at:desc")
    assert len(folders_1) == 1
    folders_2 = API.folder.get(limit=2, sort="created_at:asc")
    assert len(folders_2) == 2
    assert folders_1[0]["name"] is not folders_2[0]["name"]
    with pytest.raises(Exception):
        API.folder.get_folders(limit=1, sort="created_ats:desc")
