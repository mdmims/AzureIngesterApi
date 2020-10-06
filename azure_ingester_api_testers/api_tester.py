import flask
import json
import requests
import os


API_LOCAL_URL = 'http://localhost:5000'


class APITester(object):
    def __init__(self, url=API_LOCAL_URL, config=flask.config.import_string(os.getenv('API_ENVIRONMENT'))):
        self.url = url
        # self.headers = {'Authorization': f'Bearer {self.auth_token}'}
        # self.json_headers = {'Authorization': f'Bearer {self.auth_token}', 'Content-Type': 'application/json'}

    def post(self, uri, request_body=None):
        data = json.dumps(request_body) if request_body else None
        headers = self.json_headers if data else self.headers
        response = requests.post(self.url + uri, headers=headers, data=data, verify=False)
        response.raise_for_status()
        return response.json()

    def get(self, uri):
        response = requests.get(self.url + uri, headers=self.headers, verify=False)
        response.raise_for_status()
        return response.json()
