import pytest
from tests.conf import *
from faker import Faker
from ermeo.ermeo import ErmeoV1
from ermeo.tools import ErmeoTools


@pytest.fixture(scope="module")
def fixtures():
    faker = Faker()
    data = {
        'fake_username': faker.first_name(),
        'fake_password': "".join(faker.random_letters(length=faker.random_int(min=0, max=99, step=1))),
        'fake_access_token': "".join(faker.random_letters(length=faker.random_int(min=0, max=99, step=1))),
    }
    return data


def test_get_tokens(fixtures):
    api = ErmeoV1(api_ermeo_url=API_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, password=PASSWORD).auth.get_tokens()
    assert api.access_token
    with pytest.raises(ValueError):
        ErmeoV1(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=fixtures["fake_username"],
                  password=fixtures["fake_password"]).auth.get_tokens()


def test_set_access_token(fixtures):
    # we get the good token
    api = ErmeoV1(api_ermeo_url=API_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, password=PASSWORD).auth.get_tokens()
    test_good_token = ErmeoTools.check_access_token(api)
    assert test_good_token == True
    good_access_token = api.access_token
    # Replace good token by a false
    api.auth.set_access_token(fixtures["fake_access_token"])
    test_false = ErmeoTools.check_access_token(api)
    assert test_false == False
    # Put again the good token
    api.auth.set_access_token(good_access_token)
    test_good_token_reset = ErmeoTools.check_access_token(api)
    assert test_good_token_reset == True
