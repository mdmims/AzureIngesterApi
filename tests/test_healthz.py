import json
import os
from .base import BaseTestCase
from tests.fixtures import fixture_healthz
from azure_ingester_api.app import db, create_app
from flask_migrate import Migrate
from flask_migrate import upgrade


class TestHealthz(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        app = create_app(os.getenv('API_ENVIRONMENT', 'azure_ingester_api.config.TestConfig'))
        app.app_context().push()
        Migrate(app, db)
        upgrade()

    def setUp(self):
        pass
        # self.auth_token = jwt.encode({'sub': 'TESTS'}, self.app.config['JWT_SECRET']).decode('utf-8')

    def tearDown(self):
        db.session.remove()

    def test_ping(self):
        response = self.client.get('/healthz/ping')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual('OK', data['status'])
        self.assertEqual('PONG!', data['data'])

    def test_secured_helloworld(self):
        fixture_healthz.HelloWorldFactory.create_batch(1)

        response = self.client.get('/healthz/helloworld')
        self.assert200(response)

        data = json.loads(response.data.decode())
        self.assertEqual(len(data['data']), 2)
        self.assertEqual('OK', data['status'])
        self.assertEqual('Hello, World 1', data['data'][1]['saying'])
