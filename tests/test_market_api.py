# pylint: disable=E1123
from utils.market_api import MarketApi
from utils.data.item_meta_data import ItemMetaData
from utils.data.market_values import MarketValues
from utils.data.world_data import WorldData
from utils.json_helper import object_to_json
import pytest
from pytest_httpx import HTTPXMock
from datetime import datetime
import asyncio


class TestMarketApi:
    """Test class for the MarketApi class."""
    api = None

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self, httpx_mock: HTTPXMock):
        """Setup the MarketApi object for testing."""
        self._mock_requests(httpx_mock)
        self.api = MarketApi("asdf", force_new=True)

    @pytest.mark.parametrize("identifier", [
        " tibia coin",
        "  TiBi'A CoIN (SOMETHING) ",
        "22118  ",
        " tibia    coin   (22118)  ",
        22118
    ])
    async def test_get_meta_data_valid_identifier(self, identifier: str):
        """Test the get_meta_data method with valid identifiers."""
        # Act
        meta_data = await self.api.get_meta_data(identifier)

        # Assert
        assert meta_data.id == 22118

    async def test_get_meta_data_invalid_identifier_throws(self):
        """Test the get_meta_data method with an invalid identifier."""
        # Act & Assert
        with pytest.raises(ValueError):
            await self.api.get_meta_data("invalid identifier")

    async def test_get_market_values_valid_identifier(self):
        """Test the get_market_values method with valid identifiers."""
        # Act
        market_values = await self.api.get_market_values("Antica", 22118)

        # Assert
        assert market_values.id == 22118

    async def test_get_market_values_outdated_values_reloads(self, httpx_mock: HTTPXMock):
        """Test the get_market_values method with outdated values."""
        # Arrange
        market_values = await self.api.get_market_values("Antica", 22118)

        # Invalidate the world data cache.
        await asyncio.sleep(0.1)
        self.api.world_data.invalidate()

        new_world_data = [WorldData(name="Antica", last_update=datetime.now())]
        new_market_values = [MarketValues(id=22118, time=1)]
        httpx_mock.add_response(url="https://api.tibiamarket.top:8001/world_data", text=object_to_json(new_world_data))
        httpx_mock.add_response(url="https://api.tibiamarket.top:8001/market_values?server=Antica&limit=5000", text=object_to_json(new_market_values))

        # Act
        market_values_new = await self.api.get_market_values("Antica", 22118)

        # Assert
        assert market_values.time == 0
        assert market_values_new.time == 1

    async def test_get_market_values_without_outdated_values_does_not_reload(self, httpx_mock: HTTPXMock):
        """Test the get_market_values method with outdated but still cached values."""
        # Arrange
        market_values = await self.api.get_market_values("Antica", 22118)

        # World data is still cached and shouldn't trigger a reload.
        await asyncio.sleep(0.1)

        new_world_data = [WorldData(name="Antica", last_update=datetime.now())]
        new_market_values = [MarketValues(id=22118, time=1)]
        httpx_mock.add_response(url="https://api.tibiamarket.top:8001/world_data", text=object_to_json(new_world_data))
        httpx_mock.add_response(url="https://api.tibiamarket.top:8001/market_values?server=Antica&limit=5000", text=object_to_json(new_market_values))

        # Act
        market_values_new = await self.api.get_market_values("Antica", 22118)

        # Assert
        assert market_values.time == 0
        assert market_values_new.time == 0

    def _mock_requests(self, httpx_mock: HTTPXMock):
        item_metadata_response = [ItemMetaData(id=22118, name="tibia coin", wiki_name="Tibia Coin (Something)", npc_buy=[], npc_sell=[])]
        market_values_response = [MarketValues(id=22118, time=0)]
        world_data_response = [WorldData(name="Antica", last_update=datetime.now())]

        httpx_mock.add_response(url="https://api.tibiamarket.top:8001/item_metadata", text=object_to_json(item_metadata_response))
        httpx_mock.add_response(url="https://api.tibiamarket.top:8001/market_values?server=Antica&limit=5000", text=object_to_json(market_values_response))
        httpx_mock.add_response(url="https://api.tibiamarket.top:8001/world_data", text=object_to_json(world_data_response))
