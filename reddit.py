import requests
import os

class Reddit:
    """
    A class to interact with the Reddit API using OAuth 2.0 authentication.

    Attributes:
        url (str): The URL to obtain the access token.
        reddit_username (str): The Reddit username used to authenticate.
        reddit_password (str): The Reddit password used to authenticate.
        client_id (str): The Reddit application client ID.
        client_secret (str): The Reddit application client secret.
        access_token (str): The OAuth 2.0 access token for authentication.
        api_route (str): The base URL for making authenticated API calls.

    Methods:
        __init__: Initializes the Reddit instance and generates an OAuth token.
        generate_token: Obtains the access token using the 'password' grant type.
        get_call: Makes a GET request to the Reddit API with the provided path and parameters.
    """

    def __init__(self):
        self.url = "https://www.reddit.com/api/v1/access_token"
        self.reddit_username = os.getenv('REDDIT_USERNAME')
        self.reddit_password = os.getenv('REDDIT_PASSWORD')
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.access_token = ""
        self.api_route = "https://oauth.reddit.com"

        self.generate_token()

    def generate_token(self):
        """
        Generates an OAuth 2.0 access token for authenticating API requests.

        This method sends a POST request to Reddit's token URL with the user's credentials and
        the application's client ID and client secret. It stores the access token in the
        `access_token` attribute.

        Raises:
            requests.exceptions.RequestException: If the request to generate the token fails.
        """
        data = {
            "grant_type": "password",
            "username": self.reddit_username,
            "password": self.reddit_password,
        }

        auth = (self.client_id, self.client_secret)
        headers = {"User-Agent": "MyApp/1.0"}

        response = requests.post(self.url, data=data, auth=auth, headers=headers)

        # Check if the response was successful
        if response.status_code == 200:
            self.access_token = response.json().get("access_token", "")
        else:
            raise requests.exceptions.RequestException("Failed to obtain access token.")

    def get_call(self, path, params=""):
        """
        Makes a GET request to the Reddit API.

        This method sends a GET request to the Reddit API with the provided path and query parameters,
        and includes the OAuth 2.0 access token for authentication.

        Args:
            path (str): The API endpoint path to send the GET request to.
            params (str, optional): Query parameters to be appended to the URL. Defaults to an empty string.

        Returns:
            dict: The response JSON data from the Reddit API.

        Raises:
            requests.exceptions.RequestException: If the GET request fails.
        """
        headers = {
            "Authorization": "bearer " + self.access_token,
            "User-Agent": "ChangeMeClient/0.1 by YourUsername"
        }
        response = requests.get(self.api_route + path + params, headers=headers)

        # Check if the response was successful
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.exceptions.RequestException(f"Failed to make GET request: {response.status_code}")
