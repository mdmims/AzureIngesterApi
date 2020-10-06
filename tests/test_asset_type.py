import json

from .base import BaseTestCase


class TestDataAssetTypes(BaseTestCase):

    def setUp(self):
        pass

    def test_should_retrieve_array_of_types(self):
        response = self.client.get('/v1/AssetTypes')
        self.assert200(response)

        data = json.loads(response.data.decode())
        self.assertGreaterEqual(len(data), 1)
        self.assert_has_keys(('status', 'messages', 'code', 'result'), data)
        self.assert_has_keys(('id', 'name', 'description'), data['result']['assetTypes'][0])
        self.assert_has_standard_response_container(data)
        self.assertGreaterEqual(len(data['result']['assetTypes'][0]), 1)
