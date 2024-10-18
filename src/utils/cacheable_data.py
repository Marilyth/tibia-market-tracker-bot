import time
import asyncio
from typing import Generic, TypeVar, Callable
from utils import background_loop


T = TypeVar("T")

class CacheableData(Generic[T]):
    """A class to cache data that is loaded from a loader function. The data can be reloaded based on a predicate or a time interval.

    Args:
        loader (Callable[[], T]): The function that loads the data.
        reload_predicate (Callable[[], bool], optional): The function that determines if the data needs to be reloaded. Defaults to None.
        invalidate_after_seconds (float, optional): The time interval in seconds after which the data needs to be reloaded. Defaults to -1.
        delete_after_interval (bool, optional): Whether to automatically delete the data cache after the interval has passed. Defaults to False.
    """
    def __init__(self, loader: Callable[[], T], reload_predicate: Callable[[], bool] = None, invalidate_after_seconds: float = -1, delete_after_interval: bool = False):
        self._value: T = None
        self._was_loaded: bool = False
        self._last_load_time: float = 0
        self._loader: Callable[[], T] = loader
        self._reload_predicate: Callable[[], T] = reload_predicate if reload_predicate else lambda: False
        self._reload_interval_seconds: float = invalidate_after_seconds
        self._is_async = asyncio.iscoroutinefunction(loader) or asyncio.iscoroutinefunction(reload_predicate)
        self._is_loop_running = False
        self._delete_after_interval = delete_after_interval
        self._checker_lock = asyncio.Lock()

    @property
    def value(self) -> T:
        """Gets the current value of the cache."""
        return self._value if self._was_loaded else None

    @value.setter
    def value(self, value: T):
        if value != self.value:
            self._value = value
            self._was_loaded = True
            self._last_load_time = time.time()

            if not self._is_loop_running and self._delete_after_interval and self._reload_interval_seconds > -1:
                background_loop.run_in_background(self._check_expired_loop_async)

    def invalidate(self):
        """Invalidates the cache, causing the data to be reloaded on the next get call."""
        if not self._was_loaded:
            return

        del self._value
        self._was_loaded = False
        self._last_load_time = 0

    def get(self, new_data_time: float = -1) -> T:
        """Returns the value of the cache item. If the value needs to be (re)loaded, it will be done so.

        Args:
            new_data_time (float, optional): The timestamp of new available data.
                If the data is newer than the last load time, the data will be reloaded. Defaults to -1.

        Returns:
            T: The value of the cache item.
        """
        if self._is_async:
            raise ValueError("Loader or predicate function is async. Call get_async instead!")

        self._check_expired()
        predicate_result = self._reload_predicate()

        # Check if the value needs to be (re)loaded.
        # Because this is not async, we can skip the lock.
        if not self._was_loaded or \
           new_data_time > self._last_load_time or \
           predicate_result:
            self.value = self._loader()

        return self.value

    async def get_async(self, new_data_time: float = -1) -> T:
        """Returns the value of the cache item. If the value needs to be (re)loaded, it will be done so.

        Args:
            new_data_time (float, optional): The timestamp of new available data.
                If the data is newer than the last load time, the data will be reloaded. Defaults to -1.

        Returns:
            T: The value of the cache item.
        """
        self._check_expired()
        predicate_result = self._reload_predicate()

        if asyncio.iscoroutine(predicate_result):
            predicate_result = await predicate_result

        # Check if the value needs to be (re)loaded.
        async with self._checker_lock:
            if not self._was_loaded or \
               new_data_time > self._last_load_time or \
               predicate_result:
                self.value = self._loader()

                if asyncio.iscoroutine(self.value):
                    self.value = await self.value

        return self.value

    async def _check_expired_loop_async(self):
        """Checks in a loop if the cache item is expired, and deletes the value if it is."""
        async with self._checker_lock:
            if self._is_loop_running:
                return

            self._is_loop_running = True

        while True:
            expires_in = self._check_expired()

            if expires_in <= 0:
                break

            # Sleep until the next expiry, but at least 100ms to prevent busy waiting.
            await asyncio.sleep(max(expires_in, 0.1))

        self._is_loop_running = False

    def _check_expired(self) -> float:
        current_time: float = time.time()
        time_passed = current_time - self._last_load_time

        if self._reload_interval_seconds > -1 and time_passed >= self._reload_interval_seconds:
            self.invalidate()

        return self._reload_interval_seconds - time_passed
