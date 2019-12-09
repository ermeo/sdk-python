import requests
from ..const import API_ERMEO_FOLDER_URL, API_LIMIT, API_SORT_DEFAULT
from ..ermeo import ErmeoV1


class User:
    """
    @param ermeo_v1: ErmeoV1
    """
    def __init__(self, ermeo_v1:ErmeoV1):
        self.ermeo_v1 = ermeo_v1
        self.API_FOLDER_URL = self.ermeo_v1.api_ermeo_ressources_url + API_ERMEO_FOLDER_URL

    def create_folder(self, name, parend_id=False):
        """
        Create a folder, it's possible to set a parent, and simulate a Tree.
        @param name: string
        @param parend_id: uuid4
        @return: Json
        """
        if not parend_id:
            data = {"name": name, "resource": {"type": "document"}}
        else:
            data = {
                "name": name,
                "parent": {"id": parend_id},
                "resource": {"type": "document"},
            }

        r = requests.post(self.API_FOLDER_URL, json=data, headers=self.ermeo_v1.auth.get_headers())
        self.ermeo_v1.check_request(r)
        return r.json()

    def get_folders(self, folders=None, page=1, recursive=False, limit=API_LIMIT, sort=API_SORT_DEFAULT):
        """
        Get All Folders of the current Client
        @param folders: list
        @param page: int
        @param recursive: boolean
        @param limit: int
        @param sort: int
        @return: List
        """
        _folders = folders if folders else []
        r = requests.get(
            self.API_FOLDER_URL,
            headers=self.ermeo_v1.auth.get_headers(),
            params={"page": page, "limit": limit, "sort": sort},
        )
        self.ermeo_v1.check_request(r)
        data = r.json()
        if "items" in data:
            items = data["items"]

            for item in items:
                _folders.append(item)

            if data["next_page"] and recursive:
                next_page = page + 1
                self.get_folders(_folders, next_page, True)

        return _folders
