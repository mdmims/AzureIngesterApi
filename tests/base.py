import os
from flask_testing import TestCase
from azure_ingester_api.app import create_app


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app(os.getenv('API_ENVIRONMENT'))
        return app

    def assert_has_keys(self, expected_keys, container):
        if not isinstance(expected_keys, tuple):
            expected_keys = (expected_keys, )
        self.assertEqual(str(sorted(expected_keys)), str(sorted(container.keys())))

    def assert_has_standard_response_container(self, data, expected_status='OK', expected_code=200,
                                               expected_messages=None):
        if expected_messages is None:
            expected_messages = []
        if expected_status == 'OK':
            expected_keys = ('code', 'status', 'messages', 'result')
        else:
            expected_keys = ('code', 'status', 'messages')
        self.assert_has_keys(expected_keys, data)
        self.assertEqual(expected_status, data['status'])
        self.assertEqual(expected_code, data['code'])
        self.maxDiff = None
        self.assertEqual(str(expected_messages), str(data['messages']))
        if 'result' in expected_keys:
            self.assertGreaterEqual(len(data['result']), 1, 'Expected one or more result objects if status is OK')


class APITestCase(BaseTestCase):
    def setUp(self):
        self.maxDiff = None
        # self.headers = {"Authorization": f"Bearer {self.auth_token}", "Content-Type": "application/json"}
        # self.headers_no_content_type = {"Authorization": f"Bearer {self.auth_token}"}
        # self.api = api_client_tester.APIClientTester(self.app, self.client)
