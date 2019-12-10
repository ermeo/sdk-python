from ..const import API_ERMEO_USER_URL
from ..ermeo import ErmeoV1
from ..resource import Resource
from ..schema.user_schema import UserSchema


class User(Resource):
    """
    @param ermeo_v1: ErmeoV1
    """

    def __init__(self, ermeo_v1: ErmeoV1):
        self.ermeo_v1 = ermeo_v1
        super().__init__(ermeo_v1, self.ermeo_v1.api_ermeo_ressources_url + API_ERMEO_USER_URL, UserSchema)
