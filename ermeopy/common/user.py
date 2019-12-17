import requests
from ..const import API_ERMEO_USER_URL, API_ERMEO_ROLE_URL, API_ERMEO_TEAM_URL, API_ERMEO_ACCESS_RIGHT_URL
from ..ermeo import ErmeoV1
from ..resource import Resource
from ..schema.user_schema import UserSchema, UserSchemaUpdate, RoleSchema, RoleSchemaUpdate, AccessRightSchema, \
    AccessRightSchemaUpdate, TeamSchema, TeamSchemaUpdate

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
        super().__init__(ermeo_v1, self.ermeo_v1.api_ermeo_ressources_url + API_ERMEO_USER_URL, UserSchema,
                         UserSchemaUpdate)

    def delete(self, search_dict: dict, raw: bool = False):
        raise NotImplementedError

    def set_password(self, id: str, password: str):
        r = requests.post(self.api_ressource_url + '/' + id + '/password/update', json={'password': password},
                         headers=self.ermeo_v1.auth.get_headers())
        self.ermeo_v1.check_request(r)
        return r.json()

    def profil(self, id: str):
        r = requests.get(self.api_ressource_url + '/' + id, headers=self.ermeo_v1.auth.get_headers())
        self.ermeo_v1.check_request(r)
        return r.json()


class Role(Resource):
    """
    @param ermeo_v1: ErmeoV1
    """

    def __init__(self, ermeo_v1: ErmeoV1):
        self.ermeo_v1 = ermeo_v1
        super().__init__(ermeo_v1, self.ermeo_v1.api_ermeo_ressources_url + API_ERMEO_ROLE_URL, RoleSchema,
                         RoleSchemaUpdate)

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
        super().__init__(ermeo_v1, self.ermeo_v1.api_ermeo_ressources_url + API_ERMEO_ACCESS_RIGHT_URL,
                         AccessRightSchema, AccessRightSchemaUpdate)

    def search(self, search_dict: dict, raw: bool = False):
        raise NotImplementedError


class Team(Resource):
    """
    @param ermeo_v1: ErmeoV1
    """

    def __init__(self, ermeo_v1: ErmeoV1):
        self.access_right: AccessRight = None
        self.ermeo_v1 = ermeo_v1
        super().__init__(ermeo_v1, self.ermeo_v1.api_ermeo_ressources_url + API_ERMEO_TEAM_URL, TeamSchema,
                         TeamSchemaUpdate)
