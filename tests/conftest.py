import os

import pytest

from azure_ingester_api.api.models import AssetType
from azure_ingester_api.app import create_app


@pytest.fixture(scope="session")
def app():
    a = os.environ.get("API_ENVIRONMENT", "azure_ingester_api.config.TestConfig")
    app = create_app(environment_config=a)
    yield app


@pytest.fixture(scope="session")
def client(app):
    app.testing = True
    return app.test_client()


@pytest.fixture(scope="session")
def helpers():
    return TestHelpers()


class TestHelpers:
    """
    Helper functions used for repeat testing scenarios on individual tests
    """
    @staticmethod
    def assert_has_keys(expected_keys, container):
        if not isinstance(expected_keys, tuple):
            expected_keys = (expected_keys, )
        assert str(sorted(expected_keys)) == str(sorted(container.keys()))

    def assert_has_standard_response_container(self, data, expected_status='OK', expected_code=200, expected_messages=None):
        if expected_messages is None:
            expected_messages = []
        if expected_status == 'OK':
            expected_keys = ('code', 'status', 'messages', 'result')
        else:
            expected_keys = ('code', 'status', 'messages')
        self.assert_has_keys(expected_keys, data)
        assert expected_status == data["status"]
        assert expected_code == data["code"]
        assert str(expected_messages) == str(data["messages"])

        if "result" in expected_keys:
            assert len(data['result']) >= 1, "Expected one or more result objects if status is OK"


@pytest.fixture(scope='module')
def new_asset():
    """
    Create and populate the AssetType model with a test record
    """
    asset = AssetType(id=1, name="test_asset", description="test_asset for unit tests")
    return asset
