from utils.cache_item import CacheableData
import time


class TestCacheableData:
    """Test class for the CacheableData class."""

    def test_get_with_interval(self):
        """Test the get method with a reload interval."""
        # Arrange
        cacheable_data = CacheableData(self._get_value, reload_interval_seconds=0.5)

        # Act
        value_a = cacheable_data.get()
        value_b = cacheable_data.get()
        time.sleep(0.5)
        value_c = cacheable_data.get()

        # Assert
        assert value_a == value_b
        assert value_a != value_c

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
            return time.time() - start_time >= 0.5

        cacheable_data = CacheableData(self._get_value, reload_predicate=predicate)

        # Act
        value_a = cacheable_data.get()
        value_b = cacheable_data.get()
        time.sleep(0.5)
        value_c = cacheable_data.get()

        # Assert
        assert value_a == value_b
        assert value_a != value_c

    def _get_value(self):
        return time.time()
