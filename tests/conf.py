from decouple import config
from ermeopy.ermeo import ErmeoV1

USERNAME = config('API_ERMEO_USERNAME')
PASSWORD = config('API_ERMEO_PASSWORD')
API_URL = config('API_ERMEO_URL')
CLIENT_ID = config('ERMEO_CLIENT_ID')
CLIENT_SECRET = config('ERMEO_CLIENT_SECRET')
SLEEP = int(config('SLEEP'))

API = ErmeoV1(api_ermeo_url=API_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, password=PASSWORD).auth.get_tokens()
