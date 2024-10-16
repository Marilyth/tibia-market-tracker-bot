import time
from typing import Generic, TypeVar, Callable


T = TypeVar("T")

class CacheableData(Generic[T]):
    """A class to cache data that is loaded from a loader function. The data can be reloaded based on a predicate or a time interval.
    """
    def __init__(self, loader: Callable[[], T], reload_predicate: Callable[[], bool] = None, reload_interval_seconds: float = -1):
        self.value: T = None
        self.was_loaded: bool = False
        self.last_load_time: float = 0
        self.loader: Callable[[], T] = loader
        self.reload_predicate: Callable[[], T] = reload_predicate if reload_predicate else lambda: False
        self.reload_interval_seconds: float = reload_interval_seconds

    def get(self, new_data_time: float = -1) -> T:
        """Returns the value of the cache item. If the value needs to be (re)loaded, it will be done so.

        Args:
            new_data_time (float, optional): The timestamp of new available data.
                If the data is newer than the last load time, the data will be reloaded. Defaults to -1.

        Returns:
            T: The value of the cache item.
        """
        current_time: float = time.time()
        time_passed = current_time - self.last_load_time

        # Check if the value needs to be (re)loaded.
        if not self.was_loaded or \
            new_data_time > self.last_load_time or \
           (self.reload_interval_seconds > -1 and time_passed >= self.reload_interval_seconds) or \
           self.reload_predicate():
            self.value = self.loader()
            self.last_load_time = new_data_time if new_data_time > -1 else current_time
            self.was_loaded = True

        return self.value
