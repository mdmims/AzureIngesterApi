import json

import pytest


def test_should_retrieve_array_of_types(client, helpers):
    response = client.get('/v1/AssetTypes')
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert len(data) > 1
    helpers.assert_has_keys(('status', 'messages', 'code', 'result'), data)
    helpers.assert_has_keys(('id', 'name', 'description'), data['result']['assetTypes'][0])
    helpers.assert_has_standard_response_container(data)
    assert len(data['result']['assetTypes'][0]) >= 1


@pytest.mark.parametrize("asset_type_value, expected_status_code", [
    ("1", 200),
    ("999999999999", 404),  # out of range value
    ("not valid id", 404)  # non-int value
])
def test_retrieving_asset_types(client, helpers, asset_type_value, expected_status_code):
    response = client.get(f'/v1/AssetTypes/{asset_type_value}')
    assert response.status_code == expected_status_code
    if not 400 <= expected_status_code < 500:
        data = json.loads(response.data.decode())
        helpers.assert_has_keys(('status', 'messages', 'code', 'result'), data)
        helpers.assert_has_keys('assetType', data['result'])
        helpers.assert_has_keys(('id', 'name', 'description'), data['result']['assetType'])
