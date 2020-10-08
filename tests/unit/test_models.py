from azure_ingester_api.api import models as m


def test_asset_model(new_asset):
    """
    Test when a new AssetType is created the fields 'id' and 'name' are correctly defined
    """
    assert new_asset.id == 1
    assert new_asset.name == "test_asset"
