from utils.market_api import MarketApi
from utils.data.item_meta_data import ItemMetaData
from utils.data.market_values import MarketValues
from utils.data.world_data import WorldData
from utils.json_helper import object_to_json
import pytest
from datetime import datetime


class TestMarketApi:
    """Test class for the MarketApi class."""

    @classmethod
    def setup_class(cls):
        """Setup the MarketApi object for testing."""
        cls.api = MarketApi("asdf")

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
    def test_get_meta_data_valid_identifier(self, requests_mock, identifier: str):
        """Test the get_meta_data method with valid identifiers."""
        # Arrange
        self._mock_requests(requests_mock)

        # Act
        meta_data = self.api.get_meta_data(identifier)

        # Assert
        assert meta_data.id == 22118

    def test_get_meta_data_invalid_identifier_throws(self, requests_mock):
        """Test the get_meta_data method with an invalid identifier."""
        # Arrange
        self._mock_requests(requests_mock)

        # Act & Assert
        with pytest.raises(ValueError):
            self.api.get_meta_data("invalid identifier")

    def test_get_market_values_valid_identifier(self, requests_mock):
        """Test the get_market_values method with valid identifiers."""
        # Arrange
        self._mock_requests(requests_mock)

        # Act
        market_values = self.api.get_market_values("Antica", 22118)

        # Assert
        assert market_values.id == 22118

    def test_get_market_values_outdated_values_reloads(self, requests_mock):
        """Test the get_market_values method with outdated values."""
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

    def test_get_market_values_without_outdated_values_does_not_reload(self, requests_mock):
        """Test the get_market_values method with outdated but still cached values."""
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
