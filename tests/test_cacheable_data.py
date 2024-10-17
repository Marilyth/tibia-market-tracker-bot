from utils.cache_item import CacheableData
import time
import pytest
import asyncio


class TestCacheableData:
    """Test class for the CacheableData class."""

    def test_get_with_interval(self):
        """Test the get method with a reload interval."""
        # Arrange
        cacheable_data = CacheableData(self._get_value, invalidate_after_seconds=0.1)

        # Act
        value_a = cacheable_data.get()
        value_b = cacheable_data.get()
        time.sleep(0.1)
        value_c = cacheable_data.get()

        # Assert
        assert value_a == value_b
        assert value_a != value_c

    @pytest.mark.asyncio
    async def test_delete_with_interval(self):
        """Test if the cache is deleted after the interval."""
        # Arrange
        cacheable_data = CacheableData(self._get_value, invalidate_after_seconds=0.1, delete_after_interval=True)

        # Act
        value_a = cacheable_data.get()
        time.sleep(0.2)
        value_b = cacheable_data.value

        # Assert
        assert value_a is not None
        assert value_b is None

    @pytest.mark.asyncio
    async def test_no_delete_with_interval(self):
        """Test if the cache is not deleted after the interval."""
        # Arrange
        cacheable_data = CacheableData(self._get_value, invalidate_after_seconds=0.1, delete_after_interval=False)

        # Act
        value_a = cacheable_data.get()
        time.sleep(0.2)
        value_b = cacheable_data.value

        # Assert
        assert value_a == value_b

    def test_get_with_new_data_time(self):
        """Test the get method with new data time."""
        # Arrange
        start_time = time.time()
        cacheable_data = CacheableData(self._get_value)

        # Act
        value_a = cacheable_data.get(start_time)
        value_b = cacheable_data.get(start_time)
        time.sleep(0.01)
        value_c = cacheable_data.get(time.time())

        # Assert
        assert value_a == value_b
        assert value_a != value_c

    def test_get_with_predicate(self):
        """Test the get method with a reload predicate."""
        # Arrange
        start_time = time.time()

        def predicate():
            return time.time() - start_time >= 0.1

        cacheable_data = CacheableData(self._get_value, reload_predicate=predicate)

        # Act
        value_a = cacheable_data.get()
        value_b = cacheable_data.get()
        time.sleep(0.1)
        value_c = cacheable_data.get()

        # Assert
        assert value_a == value_b
        assert value_a != value_c

    @pytest.mark.asyncio
    async def test_get_async_with_interval(self):
        """Test the get_async method with a reload interval."""
        # Arrange
        cacheable_data = CacheableData(self._get_value_async, invalidate_after_seconds=0.1)

        # Act
        value_a = await cacheable_data.get_async()
        value_b = await cacheable_data.get_async()
        time.sleep(0.1)
        value_c = await cacheable_data.get_async()

        # Assert
        assert value_a == value_b
        assert value_a != value_c

    @pytest.mark.asyncio
    async def test_get_async_with_sync_loader(self):
        """Test the get method with a reload predicate."""
        # Arrange
        start_time = time.time()

        def predicate():
            return time.time() - start_time >= 0.1

        cacheable_data = CacheableData(self._get_value, reload_predicate=predicate)

        # Act
        value_a = await cacheable_data.get_async()
        value_b = await cacheable_data.get_async()
        time.sleep(0.1)
        value_c = await cacheable_data.get_async()

        # Assert
        assert value_a == value_b
        assert value_a != value_c

    def _get_value(self):
        return time.time()

    async def _get_value_async(self):
        return time.time()
