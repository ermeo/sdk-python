from ..const import API_ERMEO_FOLDER_URL, API_LIMIT, API_SORT_DEFAULT
from ..ermeo import ErmeoV1
from ..resource import Resource
from ..schema.folder_schema import FolderSchema


class Folder(Resource):
    """
    @param ermeo_v1: ErmeoV1
    """

    def __init__(self, ermeo_v1: ErmeoV1):
        self.ermeo_v1 = ermeo_v1
        super().__init__(ermeo_v1, self.ermeo_v1.api_ermeo_ressources_url + API_ERMEO_FOLDER_URL, FolderSchema)

    def get(self, page: int = 1, limit: int = API_LIMIT, sort: str = API_SORT_DEFAULT, recursive: bool = False,
            items: str = None, raw: bool = False):
        """
        Override the get, we can use recursive for getting all items on subdirectory
        :param page:
        :param limit:
        :param sort:
        :param recursive:
        :param items:
        :param raw:
        :return:
        """
        
        ## we must use raw for parsing loop in recursive mode
        raw = True if recursive else raw
        _folders = items if items else []
        data = super().get(page=page, limit=limit, sort=sort, raw=raw)
        if not recursive:
            return data
        _folders = self.parse_items_loop(data, _folders, page, limit)
        return _folders


