from typing import Dict, Any, List
from utils.data.item_meta_data import ItemMetaData
from utils.data.market_values import MarketValues
from utils.data.market_board import MarketBoard
from utils.data.world_data import WorldData
from utils.cacheable_data import CacheableData
from utils.decorators.singleton import singleton
import httpx
import re


@singleton
class MarketApi:
    """A helper class to interact with the Tibia Market API.
    """

    def __init__(self, token: str = None):
        self.token = token
        self.http_client = httpx.AsyncClient()

        self.api_url = "https://api.tibiamarket.top:8001/"
        self.headers = {"Authorization": f"Bearer {self.token}"}

        self.identifier_to_id: Dict[str, int] = {}

        self.world_data: CacheableData[Dict[str, WorldData]] = CacheableData(self._load_world_data, invalidate_after_seconds=60)
        self.meta_data: CacheableData[Dict[int, ItemMetaData]] = CacheableData(self._load_meta_data, invalidate_after_seconds=3600)
        self.market_values_cache: Dict[str, CacheableData[MarketValues]] = {}
        self.history_cache: Dict[str, CacheableData[List[MarketValues]]] = {}
        self.market_board_cache: Dict[str, CacheableData[MarketBoard]] = {}

    @staticmethod
    def normalize_identifier(identifier: str) -> str:
        """Normalizes an item identifier by removing non alphanumeric characters and excess whitespace.

        Args:
            identifier (str): The identifier of the item.

        Returns:
            str: The normalized identifier.
        """
        if not identifier:
            return ""

        return re.sub(r"\s{2,}", " ", re.sub(r"[^a-z0-9 ]", "", identifier.lower().strip()))

    async def identifier_to_item_id(self, identifier: str) -> int:
        """Converts an item identifier to it's id.

        Args:
            identifier (str): The identifier of the item. Can be the id, name (id), or wiki name.

        Returns:
            int: The id of the item.
        """
        await self.meta_data.get_async()
        normalized_identifier = self.normalize_identifier(str(identifier))

        if normalized_identifier not in self.identifier_to_id:
            raise ValueError(f"Item with identifier '{normalized_identifier}' not found.")

        return self.identifier_to_id[normalized_identifier]

    async def get_market_values(self, server, identifier: str) -> MarketValues:
        """Get the market values of an item by it's identifier.

        Args:
            identifier (str): The identifier of the item.

        Returns:
            MarketValues: The market values of the item.
        """
        item_id: int = await self.identifier_to_item_id(identifier)

        if server not in self.market_values_cache:
            self.market_values_cache[server] = CacheableData(lambda: self._load_market_values(server), invalidate_after_seconds=3600)

        last_world_update = (await self.world_data.get_async())[server].last_update.timestamp()
        market_values = await self.market_values_cache[server].get_async(last_world_update)

        return market_values[item_id]

    async def get_history(self, server: str, identifier: str) -> List[MarketValues]:
        """Get the market values history of an item by it's identifier.

        Args:
            server (str): The name of the Tibia server.
            identifier (str): The identifier of the item.

        Returns:
            List[MarketValues]: The market values history of the item.
        """
        item_id: int = await self.identifier_to_item_id(identifier)
        key = f"{server}_{item_id}"

        if key not in self.history_cache:
            self.history_cache[key] = CacheableData(lambda: self._load_history(server, item_id), invalidate_after_seconds=300, delete_after_interval=True)

        last_world_update = (await self.world_data.get_async())[server].last_update.timestamp()
        history = await self.history_cache[key].get_async(last_world_update)

        return history

    async def get_market_board(self, server: str, identifier: str) -> MarketBoard:
        """Get the market board of an item by it's identifier.

        Args:
            server (str): The name of the Tibia server.
            identifier (str): The identifier of the item.

        Returns:
            MarketBoard: The market board of the item.
        """
        item_id: int = await self.identifier_to_item_id(identifier)
        key = f"{server}_{item_id}"

        if key not in self.market_board_cache:
            self.market_board_cache[key] = CacheableData(lambda: self._load_market_board(server, item_id), invalidate_after_seconds=300, delete_after_interval=True)

        last_world_update = (await self.world_data.get_async())[server].last_update.timestamp()
        market_board = await self.market_board_cache[key].get_async(last_world_update)

        return market_board

    async def get_meta_data(self, identifier: str) -> ItemMetaData:
        """Get the meta data of an item by it's identifier.

        Args:
            identifier (str): The identifier of the item. Can be the id, name (id), or wiki name.

        Returns:
            ItemMetaData: The meta data of the item.
        """
        item_id: int = await self.identifier_to_item_id(identifier)

        return (await self.meta_data.get_async())[item_id]

    async def _load_market_values(self, server: str) -> MarketBoard:
        """Loads and caches the market values of an item in a Tibia server.

        Args:
            server (str): The name of the Tibia server.

        Returns:
            MarketBoard: The market values of an item in a Tibia server.
        """
        response = await self._send_request("market_values", server=server, limit=5000)

        market_values = {}

        for item in response:
            market_values[item["id"]] = MarketValues(**item)

        return market_values

    async def _load_history(self, server: str, item_id: int) -> List[MarketValues]:
        """Loads and caches the market values history of an item in a Tibia server.

        Args:
            server (str): The name of the Tibia server.
            item_id (int): The id of the item.

        Returns:
            List[MarketValues]: The market values history of an item in a Tibia server.
        """
        response = await self._send_request("item_history", server=server, item_id=item_id)

        return [MarketValues(**item) for item in response]

    async def _load_market_board(self, server: str, item_id: int) -> MarketBoard:
        """Loads and caches the market board of an item in a Tibia server.

        Args:
            server (str): The name of the Tibia server.
            item_id (int): The id of the item.

        Returns:
            MarketBoard: The market board of an item in a Tibia server.
        """
        response = await self._send_request("market_board", server=server, item_id=item_id)

        return MarketBoard(**response)

    async def _load_world_data(self) -> Dict[str, WorldData]:
        """Loads and caches the world data of all Tibia servers.

        Returns:
            Dict[str, WorldData]: The world data of all Tibia servers.
        """
        response = await self._send_request("world_data")

        worlds = {}

        for world in response:
            worlds[world["name"]] = WorldData(**world)

        return worlds

    async def _load_meta_data(self) -> Dict[str, ItemMetaData]:
        """Loads and caches the meta data of all items.

        Returns:
            Dict[int, ItemMetaData]: The meta data of all items.
        """
        response = await self._send_request("item_metadata")

        meta_data = {}

        # Populate the meta data dictionary with each item's meta data.
        # Also populate the identifier to id dictionary with any possible identifier.
        for item in response:
            item_meta_data = ItemMetaData(**item)
            meta_data[item_meta_data.id] = item_meta_data

            self.identifier_to_id[str(item["id"])] = item_meta_data.id
            self.identifier_to_id[self.normalize_identifier(item["name"])] = item_meta_data.id
            self.identifier_to_id[self.normalize_identifier(f"{item['name']} ({item['id']})")] = item_meta_data.id

            if item["wiki_name"]:
                self.identifier_to_id[self.normalize_identifier(item["wiki_name"])] = item_meta_data.id

        return meta_data

    async def _send_request(self, endpoint: str, **query_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Send a request to the Tibia API.

        Args:
            endpoint (str): The endpoint of the API.
            query_parameters (Dict): The parameters of the request.

        Returns:
            Dict: The response of the request.
        """
        response = await self.http_client.get(self.api_url + endpoint, headers=self.headers, params=query_parameters, timeout=60)

        return response.json()
