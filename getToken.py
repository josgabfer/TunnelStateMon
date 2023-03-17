import base64
import requests
import os
from termcolor import colored
from requests.models import HTTPError
from requests.auth import HTTPBasicAuth
import http.client as http_client
import logging
import dotenv
from dotenv import dotenv_values, find_dotenv 



http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
# dotenv.load_dotenv()




def generate_auth_string():
    """Here we encode the API Secret and Key in base64 format needed for the generate_token() function to request an access token."""
    config = dotenv_values(find_dotenv())
    key = config['KEY']
    secret = config['SECRET']

    auth_string = f"{key}:{secret}"

    message_bytes = auth_string.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_auth = base64_bytes.decode('ascii')
    token_API_Type = 'TOKEN'

    return (generate_token(base64_auth, token_API_Type))
    


def generate_token(base64_auth, token_API_Type):
    """
        This module will create a new OAUTH2 token for API Queries, more information at:
        https://developer.cisco.com/docs/cloud-security/#!auth-overview
    """

    print(colored(f'Refreshing token for token type: {token_API_Type}','yellow'))

    url = "https://api.umbrella.com/auth/v2/token"
    dotenv_file = dotenv.find_dotenv()
    headers = {
        "Authorization": "Basic " + base64_auth
    }
    try:
        response = requests.request("GET", url, headers = headers)

        if response.status_code == 401 or response.status_code == 403:
            print(colored(f'Invalid credentials, please update the credentials for profile {token_API_Type}','red'))
            quit()

        else:
            token_json = response.json()
            token = token_json.get('access_token')
            dotenv.set_key(dotenv_file,token_API_Type, token)
            print(colored('Token created, saving token to .env file','yellow'))
            return token

    except HTTPError as httperror:
        print(f'HTPP error occured: {httperror}')
    except Exception as e:
        print(f'An error has occured : {e}')

