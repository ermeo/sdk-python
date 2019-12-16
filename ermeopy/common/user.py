from ..const import API_ERMEO_USER_URL, API_ERMEO_ROLE_URL, API_ERMEO_TEAM_URL, API_ERMEO_ACCESS_RIGHT_URL
from ..ermeo import ErmeoV1
from ..resource import Resource
from ..schema.user_schema import UserSchema, RoleSchema, AccessRightSchema, TeamSchema


ALL_PLATFORM_PERMISSIONS = [x for x in range(1, 74)]
ALL_APP_PERMISSIONS = [x for x in range(1001, 1028)]


class User(Resource):
    """
    @param ermeo_v1: ErmeoV1
    """

    def __init__(self, ermeo_v1: ErmeoV1):
        self.role = None
        self.team = None
        self.ermeo_v1 = ermeo_v1
        super().__init__(ermeo_v1, self.ermeo_v1.api_ermeo_ressources_url + API_ERMEO_USER_URL, UserSchema)

    def delete(self, search_dict: dict, raw: bool = False):
        raise NotImplementedError


class Role(Resource):
    """
    @param ermeo_v1: ErmeoV1
    """

    def __init__(self, ermeo_v1: ErmeoV1):
        self.ermeo_v1 = ermeo_v1
        super().__init__(ermeo_v1, self.ermeo_v1.api_ermeo_ressources_url + API_ERMEO_ROLE_URL, RoleSchema)

    def create(self, data: dict, admin: bool = False):
        data = self.set_admin_rights(data) if admin else data
        return super().create(data)

    def update(self, data: dict, id: str, admin: bool = False):
        data = self.set_admin_rights(data) if admin else data
        return super().update(data, id)

    def delete(self, search_dict: dict, raw: bool = False):
        raise NotImplementedError

    def search(self, search_dict: dict, raw: bool = False):
        raise NotImplementedError

    def set_admin_rights(self, data: dict) -> dict:
        data["platform_permission"] = ALL_PLATFORM_PERMISSIONS
        data["app_permission"] = ALL_APP_PERMISSIONS
        return data


class AccessRight(Resource):
    """
    @param ermeo_v1: ErmeoV1
    """

    def __init__(self, ermeo_v1: ErmeoV1):
        self.ermeo_v1 = ermeo_v1
        super().__init__(ermeo_v1, self.ermeo_v1.api_ermeo_ressources_url + API_ERMEO_ACCESS_RIGHT_URL, AccessRightSchema)

    def search(self, search_dict: dict, raw: bool = False):
        raise NotImplementedError


class Team(Resource):
    """
    @param ermeo_v1: ErmeoV1
    """

    def __init__(self, ermeo_v1: ErmeoV1):
        self.access_right: AccessRight = None
        self.ermeo_v1 = ermeo_v1
        super().__init__(ermeo_v1, self.ermeo_v1.api_ermeo_ressources_url + API_ERMEO_TEAM_URL, TeamSchema)
