from utils.cache_item import CacheableData
import time


class TestCacheableData:
    def test_Get_WithInterval_ReturnsExpected(self):
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

    def test_Get_WithNewDataTime_ReturnsExpected(self):
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
    
    def test_GetData_WithPredicate_ReturnsExpected(self):
        # Arrange
        start_time = time.time()
        predicate = lambda: time.time() - start_time >= 0.5
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