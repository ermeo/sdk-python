import abc
import requests
from marshmallow import Schema
from ermeopy.ermeo import ErmeoV1
from ermeopy.const import API_LIMIT, API_SORT_DEFAULT, API_SEARCH_URL


class Resource(metaclass=abc.ABCMeta):
    def __init__(self, ermeo_v1: ErmeoV1, api_ressource_url: str, schema: Schema, schema_update: Schema):
        """
        Init
        :param ermeo_v1:
        :param api_ressource_url:
        :param schema:
        """

        self.ermeo_v1 = ermeo_v1
        self.api_ressource_url = api_ressource_url
        self.schema = schema
        self.schema_update = schema_update

    def list(self, page: int = 1, limit: int = API_LIMIT, sort: str = API_SORT_DEFAULT, raw: bool = False,
            items: list = False, recursive: bool = False) -> list:
        """
        Get All item from a ressource
        @param page: int
        @param limit: int
        @param sort: int
        @param sort: int
        @param raw: bool If we want the flat list
        @param items: add previous results
        @param recursive: for iteration, and get all results in one time
        @return: List or Json from API if Raw
        """

        ## we must use raw for parsing loop in recursive mode
        raw = True if recursive else raw
        previous_items  = items if items else []
        r = requests.get(
            self.api_ressource_url,
            headers=self.ermeo_v1.auth.get_headers(),
            params={"page": page, "limit": limit, "sort": sort},
        )
        self.ermeo_v1.check_request(r)
        data = r.json()
        if not recursive:
            return data if raw else data["items"]

        recursive_items = self.parse_items_recursive(data, previous_items, page, limit)
        return recursive_items

    def get(self, id: str):
        """
        Get a resource
        @param id: str
        @return: Json
        """

        r = requests.get(self.api_ressource_url + '/' + id, headers=self.ermeo_v1.auth.get_headers())
        self.ermeo_v1.check_request(r)
        return r.json()

    def delete(self, id: str):
        """
        Get a resource
        @param id: str
        @return: Json
        """
        r = requests.delete(self.api_ressource_url + '/' + id, headers=self.ermeo_v1.auth.get_headers())
        self.ermeo_v1.check_request(r)
        return r.json()

    def parse_items_recursive(self, data: object, items: list, page: int = 1, limit: int = 10) -> list:
        """
        Parse items and loop
        :param data:
        :param items:
        :param page:
        :param limit:
        :return:
        """
        if "items" in data:
            new_items = data["items"]
            for new_item in new_items:
                items.append(new_item)
        if data["next_page"]:
            next_page = page + 1
            self.list(page=next_page, recursive=True, items=items, limit=limit)
        return items

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

    def update(self, data: dict, id: str):
        """
        Update a resource
        @param data: dict
        @param id: str
        @return: Json
        """

        validated_data = self.schema_update().load(data)
        r = requests.put(self.api_ressource_url + '/' + id, json=validated_data, headers=self.ermeo_v1.auth.get_headers())
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
