from src.utils.market_api import MarketApi
from src.utils.data.item_meta_data import ItemMetaData
from src.utils.data.market_values import MarketValues
from src.utils.data.world_data import WorldData
from src.utils.json_helper import object_to_json
import pytest
from datetime import datetime


class TestMarketApi:
    # Run this method once before testing.
    @classmethod
    def setup_class(cls):
        cls.api = MarketApi("asdf")

    # Run this method once after all tests.
    @classmethod
    def teardown_class(cls):
        del cls.api

    def _mock_requests(self, requests_mock):
        item_metadata_response = [ItemMetaData(id=22118, name="tibia coin", wiki_name="Tibia Coin (Something)", npc_buy=[], npc_sell=[])]
        market_values_response = [MarketValues(id=22118, time=0)]
        world_data_response = [WorldData(name="Antica", last_update=datetime.now())]

        requests_mock.get("https://api.tibiamarket.top:8001/item_metadata", text=object_to_json(item_metadata_response))
        requests_mock.get("https://api.tibiamarket.top:8001/market_values", text=object_to_json(market_values_response))
        requests_mock.get("https://api.tibiamarket.top:8001/world_data", text=object_to_json(world_data_response))

    @pytest.mark.parametrize("identifier", [
        " tibia coin",
        "  TiBi'A CoIN (SOMETHING) ",
        "22118  ",
        " tibia    coin   (22118)  ",
        22118
    ])
    def test_GetMetaData_WithValidIdentifier_ReturnsExpected(self, requests_mock, identifier: str):
        # Arrange
        self._mock_requests(requests_mock)

        # Act
        meta_data = self.api.get_meta_data(identifier)

        # Assert
        assert meta_data.id == 22118

    def test_GetMetaData_WithInvalidIdentifier_ThrowsValueError(self, requests_mock):
        # Arrange
        self._mock_requests(requests_mock)

        # Act & Assert
        with pytest.raises(ValueError):
            self.api.get_meta_data("invalid identifier")

    def test_GetMarketValues_WithValidIdentifier_ReturnsExpected(self, requests_mock):
        # Arrange
        self._mock_requests(requests_mock)

        # Act
        market_values = self.api.get_market_values("Antica", 22118)

        # Assert
        assert market_values.id == 22118
    
    def test_GetMarketValues_WithOutdatedValues_Reloads(self, requests_mock):
        # Arrange
        self._mock_requests(requests_mock)
        market_values = self.api.get_market_values("Antica", 22118)
        self.api.world_data.last_load_time = 1234

        new_world_data = [WorldData(name="Antica", last_update=datetime.now())]
        new_market_values = [MarketValues(id=22118, time=1)]
        requests_mock.get("https://api.tibiamarket.top:8001/world_data", text=object_to_json(new_world_data))
        requests_mock.get("https://api.tibiamarket.top:8001/market_values", text=object_to_json(new_market_values))

        # Act
        market_values_new = self.api.get_market_values("Antica", 22118)

        # Assert
        assert market_values.time == 0
        assert market_values_new.time == 1
    
    def test_GetMarketValues_WithoutOutdatedValues_DoesNotReload(self, requests_mock):
        # Arrange
        self._mock_requests(requests_mock)
        market_values = self.api.get_market_values("Antica", 22118)

        new_world_data = [WorldData(name="Antica", last_update=datetime.now())]
        new_market_values = [MarketValues(id=22118, time=1)]
        requests_mock.get("https://api.tibiamarket.top:8001/world_data", text=object_to_json(new_world_data))
        requests_mock.get("https://api.tibiamarket.top:8001/market_values", text=object_to_json(new_market_values))

        # Act
        market_values_new = self.api.get_market_values("Antica", 22118)

        # Assert
        assert market_values.time == 0
        assert market_values_new.time == 0
        