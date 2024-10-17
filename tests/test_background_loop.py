from utils.cache_item import CacheableData
import utils.background_loop as background_loop
import time
import asyncio


def test_cancel_task():
    """Test cancelling the returned object."""
    # Arrange
    values_a = []
    values_b = []

    async def async_function():
        for i in range(10):
            values_a.append(i)
            await asyncio.sleep(0.1)

    # Act
    task = background_loop.run_in_background(async_function)

    for i in range(10):
        if i == 5:
            task.cancel()

        values_b.append(i)
        time.sleep(0.1)

    # Assert
    assert values_a != values_b

def test_run_in_background_sync():
    """Test the run_in_background method with a synchronous function."""
    # Arrange
    values_a = []
    values_b = []
    time_start = time.time()

    def sync_function():
        for i in range(10):
            values_a.append(i)
            time.sleep(0.1)

    # Act
    background_loop.run_in_background(sync_function)
    for i in range(10):
        values_b.append(i)
        time.sleep(0.1)

    # Assert
    assert time_start - time.time() < 1.5
    assert values_a == values_b

def test_run_in_background_async():
    """Test the run_in_background method with an asynchronous function."""
    # Arrange
    values_a = []
    values_b = []
    time_start = time.time()

    async def async_function():
        for i in range(10):
            values_a.append(i)
            await asyncio.sleep(0.1)

    # Act
    background_loop.run_in_background(async_function)
    for i in range(10):
        values_b.append(i)
        time.sleep(0.1)

    # Assert
    assert time_start - time.time() < 1.5
    assert values_a == values_b
