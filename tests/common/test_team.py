import pytest
import random
from tests.conf import *
from faker import Faker
from time import sleep


@pytest.fixture(scope="module")
def fixtures():
    faker = Faker()
    data = {
        'team_code': "".join(faker.random_letters(length=faker.random_int(min=3, max=99, step=1))),
        'team_name': faker.job(),
        'team_users': [{'id': API.user.list()[0]['id']}, {'id': API.user.list()[1]['id']}],
        'team_leaders': [{'id': API.user.list()[0]['id']}],
        'team_access_rights': [{'id': API.user.team.access_right.list()[0]['id']},
                               {'id': API.user.team.access_right.list()[1]['id']}],

        'team_updated_code': "".join(faker.random_letters(length=faker.random_int(min=3, max=99, step=1))),
        'team_updated_name': faker.job(),
        'team_updated_users': [{'id': API.user.list()[0]['id']}, {'id': API.user.list()[1]['id']}, {'id': API.user.list()[3]['id']}],
        'team_updated_leaders': [{'id': API.user.list()[0]['id']}, {'id': API.user.list()[2]['id']}],
        'team_updated_access_rights': [{'id': API.user.team.access_right.list()[0]['id']},
                               {'id': API.user.team.access_right.list()[1]['id']}],
    }
    return data


def test_create_update_team(fixtures):
    team = {
        "code": fixtures["team_code"],
        "name": fixtures["team_name"],
        "users": fixtures["team_users"],
        "leaders": fixtures["team_leaders"],
        "access_rights": fixtures["team_access_rights"],
    }
    team_created = API.user.team.create(team)
    assert team_created["code"] == team["code"]
    assert team_created["name"] == team["name"]
    assert len(team_created["users"]) == len(team["users"])
    assert len(team_created["leaders"]) == len(team["leaders"])
    assert len(team_created["access_rights"]) == len(team["access_rights"])
    sleep(SLEEP)
    team_get = API.user.team.get(team_created["id"])
    assert team_get["code"] == fixtures["team_code"]

    team_update = {
        "code": fixtures["team_updated_code"],
        "name": fixtures["team_updated_name"],
        "users": fixtures["team_updated_users"],
        "leaders": fixtures["team_updated_leaders"],
        "access_rights": fixtures["team_updated_access_rights"],
    }
    team_updated = API.user.team.update(team_update, id=team_created["id"])
    assert team_updated["code"] == team_update["code"]
    assert team_updated["name"] == team_update["name"]
    assert len(team_updated["users"]) == len(team_update["users"])
    assert len(team_updated["leaders"]) == len(team_update["leaders"])
    assert len(team_updated["access_rights"]) == len(team_update["access_rights"])


def test_search_teams(fixtures):
    ## We sleep because the API Must reindex some results
    sleep(SLEEP)
    search_team = \
        [
            {
                "code": [
                    {
                        "operator": "equals",
                        "value": {
                            "text": fixtures["team_updated_code"]
                        }
                    }
                ]
            }
        ]
    team = API.user.team.search(search_dict=search_team)
    assert team[0]["code"] == fixtures["team_updated_code"]


def test_get_teams():
    team = API.user.team.list(limit=1, sort="created_at:desc")
    assert len(team) == 1
    teams = API.user.team.list(limit=2, sort="created_at:asc")
    assert len(teams) == 2
    assert team[0]["code"] is not teams[0]["code"]

    team_raw = API.user.team.list(limit=1, raw=True)
    team_recursive = API.user.team.list(limit=10, recursive=True)
    assert int(team_raw["total_items"]) == len(team_recursive)

    with pytest.raises(Exception):
        API.user.team.list(limit=1, sort="created_ats:desc")
