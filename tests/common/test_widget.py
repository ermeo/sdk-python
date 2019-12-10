import pytest
import random
from tests.conf import *
from faker import Faker
from time import sleep
from ermeo.schema.widget_schema import type_enum, category_enum


@pytest.fixture(scope="module")
def fixtures():
    faker = Faker()

    data = {
        'widget_code': "".join(faker.random_letters(length=faker.random_int(min=3, max=99, step=1))),
        'widget_name': "".join(faker.random_letters(length=faker.random_int(min=3, max=99, step=1))),
        'widget_icon': faker.first_name(),
        'widget_category': random.choice(category_enum),
        'widget_type': random.choice(type_enum),

        'widget_updated_code': "".join(faker.random_letters(length=faker.random_int(min=3, max=99, step=1))),
        'widget_updated_name': "".join(faker.random_letters(length=faker.random_int(min=3, max=99, step=1))),
        'widget_updated_icon': faker.first_name(),
        'widget_updated_category': random.choice(category_enum),
        'widget_updated_type': random.choice(type_enum),
    }
    return data


def test_crud_widget(fixtures):
    widget = {
        "code": fixtures["widget_code"],
        "name": fixtures["widget_name"],
        "icon": fixtures["widget_icon"],
        "category": fixtures["widget_category"],
        "type": fixtures["widget_type"],
    }
    print(widget)
    widget_created = API.widget.create(widget)

    widget = API.widget.get(id=widget_created["id"])
    assert widget["code"] == fixtures["widget_code"]

    assert widget_created["code"] == widget["code"]
    assert widget_created["name"] == widget["name"]
    assert widget_created["icon"] == widget["icon"]
    assert widget_created["category"] == widget["category"]
    assert widget_created["type"] == widget["type"]

    widget_update = {
        "code": fixtures["widget_updated_code"],
        "name": fixtures["widget_updated_name"],
        "icon": fixtures["widget_updated_icon"],
        "category": fixtures["widget_updated_category"],
        "type": fixtures["widget_updated_type"],
    }

    # We cant update category and type for now
    widget_updated = API.widget.update(widget_update, id=widget_created["id"])
    assert widget_updated["code"] == widget_update["code"]
    assert widget_updated["name"] == widget_update["name"]
    assert widget_updated["icon"] == widget_update["icon"]

    with pytest.raises(NotImplementedError):
        API.widget.delete(widget_created["id"])


def test_search_widgets(fixtures):
    ## We sleep because the API Must reindex some results
    sleep(SLEEP)
    search_user = \
        [
            {
                "code": [
                    {
                        "operator": "equals",
                        "value": {
                            "text": fixtures["widget_updated_code"]
                        }
                    }
                ]
            }
        ]
    with pytest.raises(NotImplementedError):
        API.widget.search(search_dict=search_user)


def test_list_widgets():
    sleep(SLEEP)
    widget = API.widget.list(limit=1, sort="created_at:desc")
    assert len(widget) == 1
    widgets = API.widget.list(limit=2, sort="created_at:asc")
    assert len(widgets) == 2
    assert widget[0]["code"] is not widgets[0]["code"]

    widget_raw = API.widget.list(limit=1, raw=True)
    widget_recursive = API.widget.list(limit=10, recursive=True)
    assert int(widget_raw["total_items"]) == len(widget_recursive)

    with pytest.raises(Exception):
        API.widget.list(limit=1, sort="created_ats:desc")

