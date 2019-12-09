import requests
from ermeo.const import API_ERMEO_PROFILE_URL
from ermeo.ermeo import ErmeoV1


class ErmeoTools(object):
    @staticmethod
    def check_access_token(api: ErmeoV1) -> bool:
        """
        Check if the bearer token is OK
        @param api:
        @return: bool
        """
        response = requests.get(api.api_ermeo_ressources_url + API_ERMEO_PROFILE_URL, headers=api.auth.get_headers())
        if response.status_code > 200:
            return False
        else:
            return True
