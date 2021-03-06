import json
from dataclasses import dataclass
from typing import Union

import pytest


@dataclass(frozen=False)
class PageSchema:
    page: Union[int, None] = None
    hasPrev: bool = None
    prevPageNum: Union[int, None] = None
    prevPage: Union[str, None] = None
    hasNext: bool = None
    perPage: Union[int, None] = None
    totalItems: Union[int, None] = None
    nextPageNum: Union[int, None] = None
    totalPages: Union[int, None] = None
    nextPage: Union[str, None] = None


def build_page_data_object(page_data: dict):
    output = PageSchema()
    for k, v in page_data.items():
        setattr(output, k, v)
    return output


def test_should_retrieve_array_of_types(client, helpers):
    response = client.get('/v1/assetTypes')
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
    response = client.get(f'/v1/assetTypes/{asset_type_value}')
    assert response.status_code == expected_status_code
    if not 400 <= expected_status_code < 500:
        data = json.loads(response.data.decode())
        helpers.assert_has_keys(('status', 'messages', 'code', 'result'), data)
        helpers.assert_has_keys('assetType', data['result'])
        helpers.assert_has_keys(('id', 'name', 'description'), data['result']['assetType'])


def test_should_retrieve_pagination_data_for_all_asset_types(client, helpers):
    response = client.get("/v1/assetTypes")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert "page" in data["result"]

    # instantiate class to hold expected values for page data
    expected = PageSchema(page=1, hasPrev=False, prevPageNum=None, prevPage=None, hasNext=False, perPage=20, totalItems=2,
                          nextPageNum=None, totalPages=1, nextPage=None)

    # retrieve the json response and map the values to the defined schema
    actual = build_page_data_object(data["result"]["page"])

    assert expected == actual


@pytest.mark.parametrize("expected", [PageSchema(page=1, hasPrev=False, prevPageNum=None, prevPage=None, hasNext=True, perPage=1, totalItems=2,
                         nextPageNum=2, totalPages=2, nextPage="/v1/assetTypes?page=2&perPage=1")])
def test_should_retrieve_specific_page_data(client, helpers, expected):
    """ Test retrieving 1 page of data and verify the json response for Page values"""
    response = client.get("/v1/assetTypes?page=1&perPage=1")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    actual = build_page_data_object(data["result"]["page"])
    assert expected == actual
