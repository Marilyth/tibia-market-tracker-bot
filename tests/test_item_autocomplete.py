# pylint: disable=E1123
from datetime import datetime
from pytest_httpx import HTTPXMock
from modules.autocomplete import item
from utils.market_api import MarketApi
from utils.data.item_meta_data import ItemMetaData
from utils.data.market_values import MarketValues
from utils.data.world_data import WorldData
from utils.json_helper import object_to_json
import pytest


class TestItemAutocomplete:
    """Test class for the item autocomplete function."""
    api = None

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self, httpx_mock: HTTPXMock):
        """Setup the MarketApi object for testing."""
        self._mock_requests(httpx_mock)
        MarketApi(force_new=True)

    async def test_item_autocomplete_many_results_ordered_by_length(self):
        """Test the get_meta_data method with valid identifiers."""
        # Arrange
        name = "sword"

        # Act
        choices = await item.item_autocomplete(name)

        # Assert
        assert len(choices) == 3
        assert choices[0].name == "Sword"
        assert choices[-1].name == "Magic Sword"

    async def test_item_autocomplete_non_normal_works(self):
        """Test the get_meta_data method with valid identifiers."""
        # Arrange
        name = "npcs magic things"

        # Act
        choices = await item.item_autocomplete(name)

        # Assert
        assert len(choices) == 1
        assert choices[0].name == "NPC's magic thing's strength item thingy"

    async def test_item_autocomplete_no_results(self):
        """Test the get_meta_data method with valid identifiers."""
        # Arrange
        name = "invalid"

        # Act
        choices = await item.item_autocomplete(name)

        # Assert
        assert len(choices) == 0

    async def test_item_autocomplete_no_name(self):
        """Test the get_meta_data method with valid identifiers."""
        # Arrange
        name = ""

        # Act
        choices = await item.item_autocomplete(name)

        # Assert
        assert len(choices) == 8

    def _mock_requests(self, httpx_mock: HTTPXMock):
        item_metadata_response = [
            ItemMetaData(id=1, name="tibia coin", wiki_name="Tibia Coin", npc_buy=[], npc_sell=[]),
            ItemMetaData(id=2, name="gold coin", wiki_name="Gold Coin", npc_buy=[], npc_sell=[]),
            ItemMetaData(id=3, name="platinum coin", wiki_name="Platinum Coin", npc_buy=[], npc_sell=[]),
            ItemMetaData(id=4, name="crystal coin", wiki_name="Crystal Coin", npc_buy=[], npc_sell=[]),
            ItemMetaData(id=5, name="fire sword", wiki_name="Fire Sword", npc_buy=[], npc_sell=[]),
            ItemMetaData(id=6, name="sword", wiki_name="Sword", npc_buy=[], npc_sell=[]),
            ItemMetaData(id=7, name="magic sword", wiki_name="Magic Sword", npc_buy=[], npc_sell=[]),
            ItemMetaData(id=8, name="NPC's magic thing's strength item thingy", npc_buy=[], npc_sell=[]),
        ]
        market_values_response = [MarketValues(id=22118, time=0)]
        world_data_response = [WorldData(name="Antica", last_update=datetime.now())]

        httpx_mock.add_response(url="https://api.tibiamarket.top:8001/item_metadata", text=object_to_json(item_metadata_response))
        httpx_mock.add_response(url="https://api.tibiamarket.top:8001/market_values?server=Antica&limit=5000", text=object_to_json(market_values_response))
        httpx_mock.add_response(url="https://api.tibiamarket.top:8001/world_data", text=object_to_json(world_data_response))
