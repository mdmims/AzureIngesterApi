import pytest
from azure_ingester_api.api.models import AssetType


@pytest.fixture(scope='module')
def new_asset():
    """
    Create and populate the AssetType model with a test record
    """
    asset = AssetType(id=1, name="test_asset", description="test_asset for unit tests")
    return asset
