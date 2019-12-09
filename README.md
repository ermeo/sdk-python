# Python SDK  
[![Latest Build](https://travis-ci.org/ermeo/sdk-python.svg?branch=master)](https://travis-ci.org/ermeo/sdk-python.svg?branch=master)

This is a Python client for the Ermeo Data API. The sdk-ermeo is a wrapper to simplify access to ressources requests and JSON response parsing from the API Ermeo. This package evolving with the API.


##### Install
We recommend you install this module using pip:

```
pip install sdk-ermeo
```

##### Quickstart

In order to access the API, you'll need to get a service key from Ermeo. Contact the client service.

Once you have it you can use the API key to initiate the ErmeoAPI class.

```
api = ErmeoV1(client_id='your_client_id', client_secret='your_client_secret', username='your_username', password='your_password').auth.get_tokens()
```

Then you can override some params for testing purpose : 
- api_ermeo_url = 'sandbox_url_for_example'
 
 
##### Testing

Only latest version of Ermeo are tested. You should upgrade the SDK with each new versions.

You must have environment variable or a file .env placed on root of this project with the following variable:


- API_ERMEO_USERNAME
- API_ERMEO_PASSWORD
- API_ERMEO_URL
- ERMEO_CLIENT_ID
- ERMEO_CLIENT_SECRET

Then launch tox.
```
tox
```

For testing something precisly you can do :
```
pytest -k "test_login"
```
This will test only the function "test_login"