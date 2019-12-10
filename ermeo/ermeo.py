from .const import API_ERMEO_URL, API_ERMEO_LOGIN_URL, API_ERMEO_VERSION_URL


class ErmeoV1(object):
    def __init__(
            self,
            client_id: str = False,
            client_secret: str = False,
            username: str = False,
            password: str = False,
            api_ermeo_url: str = API_ERMEO_URL,
            access_token: str = False,
            refresh_token: str = False,
    ):
        """
        Init of all variables use for the calls + Modules

        @param client_id: str
        @param client_secret: str
        @param username: str
        @param password: str
        @param api_ermeo_url: str
        @param access_token: str
        @param refresh_token: str
        """
        self.api_ermeo_url = api_ermeo_url
        self.api_ermeo_ressources_url = self.api_ermeo_url + API_ERMEO_VERSION_URL
        self.api_ermeo_login_url = self.api_ermeo_url + API_ERMEO_LOGIN_URL
        self.username = username
        self.password = password
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret

        self.load_modules()

    def load_modules(self):
        """
        # We load modules here, for avoid circular imports
        :return:
        """
        from .common.folder import Folder
        from .common.auth import Auth
        from .common.user import User

        self.folder = Folder(self)
        self.auth = Auth(self)
        self.user = User(self)

        return self

    def check_request(self, r):
        """
        Check each request, and send error if any
        @param r: Request
        @return:
        """
        if r.status_code > 202:
            raise Exception(r.content, r.status_code)
