# pylint: disable=W0201,E1101
from modules.embedder.market_values import market_value_to_embedding, sale_data_to_expression
from modules.embedder.history import history_to_embedding
from modules.embedder.market_board import market_board_to_embedding, dict_to_table
from utils.data.item_meta_data import NPCSaleData, ItemMetaData
from utils.data.market_values import MarketValues
from utils.data.market_board import MarketBoard, MarketBoardTraderData
from utils.market_api import MarketApi
from utils import GOLD_COIN_EMOJI
import pytest


class TestEmbedder:
    """Test class for the embedder functions."""

    @pytest.fixture(autouse=True, scope="function")
    def setup_class(self):
        """Setup the test class."""
        MarketApi().meta_data.value = {
            0: TestEmbedder.create_sample_item_meta_data("Gold"),
            1: TestEmbedder.create_sample_item_meta_data("Silver"),
            2: TestEmbedder.create_sample_item_meta_data("Bronze"),
        }

        self.market_values = TestEmbedder.create_sample_market_values()
        self.meta_data = TestEmbedder.create_sample_item_meta_data("Sample Item")

    def test_sale_data_to_expression(self):
        """Test the sale_data_to_expression function."""
        # Arrange
        sale_data = self.meta_data.npc_sell

        # Act
        sell_expression = sale_data_to_expression(sale_data, reverse_sorting=True, line_limit=1)
        buy_expression = sale_data_to_expression(sale_data, reverse_sorting=False, line_limit=1)

        # Assert
        assert sell_expression == "[NPC 29](https://tibia.fandom.com/wiki/NPC_29) in Location 29 for 1,550 _UnknownCurrency:29_\n_And 29 more..._"
        assert buy_expression == f"[NPC 0](https://tibia.fandom.com/wiki/NPC_0) in Location 0 for 100 {GOLD_COIN_EMOJI}\n_And 29 more..._"

    def test_market_value_to_embedding(self):
        """Test the market_value_to_embedding function."""
        # Act
        embed = market_value_to_embedding("Antica", self.market_values, self.meta_data)

        # Assert
        assert embed.description == "[Sample Item](https://tibia.fandom.com/wiki/Sample_Item) on Antica"
        assert embed.fields[0].name == "Sell data"
        assert embed.fields[1].name == "Buy data"
        assert embed.fields[2].name == "Buy from"
        assert embed.fields[3].name == "Sell to"
        assert len(embed.fields) == 4

    def test_market_value_to_embedding_without_sell_data(self):
        """Test the market_value_to_embedding function, if there is no sell data."""
        # Arrange
        self.meta_data.npc_sell = []

        # Act
        embed = market_value_to_embedding("Antica", self.market_values, self.meta_data)

        # Assert
        assert embed.description == "[Sample Item](https://tibia.fandom.com/wiki/Sample_Item) on Antica"
        assert embed.fields[0].name == "Sell data"
        assert embed.fields[1].name == "Buy data"
        assert embed.fields[2].name == "Sell to"
        assert len(embed.fields) == 3

    def test_market_value_to_embedding_without_buy_data(self):
        """Test the market_value_to_embedding function, if there is no buy data."""
        # Arrange
        self.meta_data.npc_buy = []

        # Act
        embed = market_value_to_embedding("Antica", self.market_values, self.meta_data)

        # Assert
        assert embed.description == "[Sample Item](https://tibia.fandom.com/wiki/Sample_Item) on Antica"
        assert embed.fields[0].name == "Sell data"
        assert embed.fields[1].name == "Buy data"
        assert embed.fields[2].name == "Buy from"
        assert len(embed.fields) == 3

    def test_history_to_embedding(self):
        """Test the history_to_embedding function."""
        # Arrange
        history = [self.market_values, self.market_values, self.market_values]
        history[0].day_average_sell += 200
        history[0].day_average_buy += 200
        history[0].time -= 1000

        history[1].day_average_sell += 100
        history[1].day_average_buy += 100
        history[1].time -= 500

        # Act
        embed, file = history_to_embedding("Antica", history, self.meta_data)

        # Assert
        assert embed.description == "[Sample Item](https://tibia.fandom.com/wiki/Sample_Item) on Antica"
        assert embed.fields[0].name == "Sell data"
        assert embed.fields[1].name == "Buy data"
        assert len(embed.fields) == 2
        assert file.filename == "plot.png"
        assert embed.image.url == "attachment://plot.png"

    def test_dict_to_table(self):
        """Test the dict_to_table function."""
        # Arrange
        data = [
            {"Name": "Sample Item", "Price": 100, "Location": "Town"},
            {"Name": "Sample", "Price": 100, "Location": "Town B"},
            {"Name": "Sam", "Price": 1003, "Location": "Town"},
        ]

        # Act
        table = dict_to_table(data)

        # Assert
        assert table == '```sql\nName        | Price | Location\n------------------------------\nSample Item   100     Town    \nSample        100     Town B  \nSam           1003    Town    \n```'

    def test_market_board_to_embedding(self):
        """Test the market_board_to_embedding function."""
        # Arrange
        sellers = [
            MarketBoardTraderData(name="Seller", amount=12, price=1, time=0),
            MarketBoardTraderData(name="Seller 1", amount=1, price=1, time=0),
            MarketBoardTraderData(name="Seller 2", amount=1, price=14, time=0),
        ]

        buyers = [
            MarketBoardTraderData(name="Buyer", amount=1, price=1, time=0),
            MarketBoardTraderData(name="Buyer", amount=1, price=1, time=0),
            MarketBoardTraderData(name="Buyer", amount=1, price=1, time=0),
        ]

        market_board = MarketBoard(id=1, sellers=sellers, buyers=buyers, update_time=0)

        # Act
        embed = market_board_to_embedding("Antica", market_board, self.meta_data)

        # Assert
        assert embed.description == "[Sample Item](https://tibia.fandom.com/wiki/Sample_Item) on Antica"
        assert embed.fields[0].name == "Sell offers"
        assert embed.fields[1].name == "Buy offers"
        assert len(embed.fields) == 2

    @staticmethod
    def create_sample_npc_sale_data(name="Sample NPC", location="Town", price=100, currency_id=0) -> NPCSaleData:
        """Creates a sample NPCSaleData object.
        
        Args:
            name (str, optional): The name of the NPC. Defaults to "Sample NPC".
            location (str, optional): The location of the NPC. Defaults to "Town".
            price (int, optional): The price of the item. Defaults to 100.
            currency_id (int, optional): The currency id. Defaults to 0.

        Returns:
            NPCSaleData: The sample NPCSaleData object.
        """
        return NPCSaleData(name=name, location=location, price=price, currency_object_type_id=currency_id, currency_quest_flag_display_name="")

    @staticmethod
    def create_sample_item_meta_data(name="Sample Item") -> ItemMetaData:
        """Creates a sample ItemMetaData object.
        
        Args:
            name (str, optional): The name of the item. Defaults to "Sample Item".
            
        Returns:
            ItemMetaData: The sample ItemMetaData object.
        """
        meta_data = ItemMetaData(id=1, category="Item", tier=0, npc_sell=[], npc_buy=[], name=name, wiki_name=name)

        for i in range(30):
            meta_data.npc_sell.append(TestEmbedder.create_sample_npc_sale_data(f"NPC {i}", f"Location {i}", 100 + i * 50, i))
            meta_data.npc_buy.append(TestEmbedder.create_sample_npc_sale_data(f"NPC {i}", f"Location {i}", 100 + i * 50, i))

        return meta_data

    @staticmethod
    def create_sample_market_values() -> MarketValues:
        """Creates a sample MarketValues object.

        Returns:
            MarketValues: The sample MarketValues object.
        """
        return MarketValues(
            id=1,
            time=1634169600,
            day_average_sell=150,
            sell_offer=120,
            month_sold=30,
            month_highest_sell=200,
            month_average_sell=160,
            month_lowest_sell=100,
            buy_offer=110,
            buy_offers=10,
            month_bought=25,
            month_highest_buy=180,
            month_average_buy=130,
            month_lowest_buy=90,
        )
