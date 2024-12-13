import requests
import os

class Reddit:
    def __init__(self):
        self.url = "https://www.reddit.com/api/v1/access_token"
        self.reddit_username = os.getenv('REDDIT_USERNAME')
        self.reddit_password = os.getenv('REDDIT_PASSWORD')
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.access_token = ""
        self.api_route = "https://oauth.reddit.com"

    def generate_token(self):
        data = {
            "grant_type": "password",
            "username": self.reddit_username,
            "password": self.reddit_password,
        }

        auth = (self.client_id, self.client_secret)
        headers = {"User-Agent": "MyApp/1.0"}

        response = requests.post(self.url, data=data, auth=auth, headers=headers)

        self.access_token = response.json()["access_token"]

    def get_call(self, path, params):
        headers = {"Authorization": "bearer " + self.access_token, "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
        response = requests.get(self.api_route + path + params, headers=headers)
        return response.json()
