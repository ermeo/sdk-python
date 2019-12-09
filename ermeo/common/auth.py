import requests
import json
from ..const import API_ERMEO_GRANT_TYPE
from ..ermeo import ErmeoV1


class Auth:
    """
    @param ermeo_v1: ErmeoV1
    """
    def __init__(self, ermeo_v1):
        self.ermeo_v1 = ermeo_v1

    def login(self) -> requests:
        """
        @return: requests
        """
        r = requests.post(
            self.ermeo_v1.api_ermeo_login_url,
            data={
                "username": self.ermeo_v1.username,
                "password": self.ermeo_v1.password,
                "grant_type": API_ERMEO_GRANT_TYPE,
                "client_id": self.ermeo_v1.client_id,
                "client_secret": self.ermeo_v1.client_secret,
            },
        )
        return r

    def get_tokens(self) -> ErmeoV1:
        """
        @return: ErmeoV1
        """
        r = self.login()
        if r:
            r_tokens = json.loads(r.content)
            self.ermeo_v1.access_token = r_tokens["access_token"]
            self.ermeo_v1.refresh_token = r_tokens["refresh_token"]
            return self.ermeo_v1
        else:
            raise ValueError("Login/password incorrect", r)

    def set_access_token(self, access_token: str) -> ErmeoV1:
        self.ermeo_v1.access_token = access_token
        return self.ermeo_v1

    def get_headers(self) -> dict:
        """
        @return: Dict
        """
        return {"Authorization": "Bearer " + self.ermeo_v1.access_token}


