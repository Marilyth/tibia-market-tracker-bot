# pylint: disable=E1123
from datetime import datetime
from pytest_httpx import HTTPXMock
from modules.autocomplete import world
from utils.market_api import MarketApi
from utils.data.world_data import WorldData
from utils.json_helper import object_to_json
import pytest


class TestWorldAutocomplete:
    """Test class for the world autocomplete function."""
    api = None

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self, httpx_mock: HTTPXMock):
        """Setup the MarketApi object for testing."""
        self._mock_requests(httpx_mock)
        MarketApi(force_new=True)

    async def test_world_autocomplete_many_results_ordered_by_length(self):
        """Test the get_meta_data method with valid identifiers."""
        # Arrange
        name = "ra"

        # Act
        choices = await world.world_autocomplete(name)

        # Assert
        assert len(choices) == 2
        assert choices[0].name == "Fidera"
        assert choices[-1].name == "Calmera"

    async def test_world_autocomplete_non_normal_works(self):
        """Test the get_meta_data method with valid identifiers."""
        # Arrange
        name = "EfIdiA"

        # Act
        choices = await world.world_autocomplete(name)

        # Assert
        assert len(choices) == 1
        assert choices[0].name == "Efi'dia"

    async def test_world_autocomplete_no_results(self):
        """Test the get_meta_data method with valid identifiers."""
        # Arrange
        name = "invalid"

        # Act
        choices = await world.world_autocomplete(name)

        # Assert
        assert len(choices) == 0

    async def test_world_autocomplete_no_name(self):
        """Test the get_meta_data method with valid identifiers."""
        # Arrange
        name = ""

        # Act
        choices = await world.world_autocomplete(name)

        # Assert
        assert len(choices) == 7

    def _mock_requests(self, httpx_mock: HTTPXMock):
        world_data_response = [
            WorldData(name="Antica", last_update=datetime.now()),
            WorldData(name="Bona", last_update=datetime.now()),
            WorldData(name="Calmera", last_update=datetime.now()),
            WorldData(name="Duna", last_update=datetime.now()),
            WorldData(name="Efi'dia", last_update=datetime.now()),
            WorldData(name="Fidera", last_update=datetime.now()),
            WorldData(name="Guardia", last_update=datetime.now())
        ]

        httpx_mock.add_response(url="https://api.tibiamarket.top:8001/world_data", text=object_to_json(world_data_response))
