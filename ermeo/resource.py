import abc
from ermeo.const import API_LIMIT, API_SORT_DEFAULT, API_SEARCH_URL
import requests
from ermeo.ermeo import ErmeoV1
from marshmallow import Schema


class Resource(metaclass=abc.ABCMeta):
    def __init__(self, ermeo_v1: ErmeoV1, api_ressource_url: str, schema: Schema):
        """
        Init
        :param ermeo_v1:
        :param api_ressource_url:
        :param schema:
        """

        self.ermeo_v1 = ermeo_v1
        self.api_ressource_url = api_ressource_url
        self.schema = schema

    def get(self, page: int = 1, limit: int = API_LIMIT, sort: str = API_SORT_DEFAULT, raw: bool = False) -> list:
        """
        Get All item from a ressource
        @param page: int
        @param limit: int
        @param sort: int
        @param sort: int
        @param raw: bool If we want the flat list
        @return: List
        """

        r = requests.get(
            self.api_ressource_url,
            headers=self.ermeo_v1.auth.get_headers(),
            params={"page": page, "limit": limit, "sort": sort},
        )
        self.ermeo_v1.check_request(r)
        data = r.json()
        return data if raw else data["items"]

    def create(self, data: dict):
        """
        Create a resource
        @param data: dict
        @return: Json
        """

        validated_data = self.schema().load(data)
        r = requests.post(self.api_ressource_url, json=validated_data, headers=self.ermeo_v1.auth.get_headers())
        self.ermeo_v1.check_request(r)
        return r.json()

    def search(self, search_dict: dict, raw: bool = False):
        """
        Search for a resource
        @param search_dict: dict, Search request
        @param raw: dict, Return raw results from api or not
        @return: Json
        """

        r = requests.post(self.api_ressource_url + API_SEARCH_URL, json=search_dict,
                          headers=self.ermeo_v1.auth.get_headers())
        self.ermeo_v1.check_request(r)
        data = r.json()
        return data if raw else data["items"]
