import asyncio
import threading
from typing import Callable
from asyncio import Future


_background_loop = asyncio.new_event_loop()

def get_background_loop() -> asyncio.AbstractEventLoop:
    """Gets the background loop.
    
    Returns:
        asyncio.AbstractEventLoop: The background loop.
    """
    if not _background_loop.is_running():
        threading.Thread(target=_background_loop.run_forever).start()

    return _background_loop

def run_in_background(func: Callable) -> Future:
    """Runs a callable in a background thread.
    If it is a coroutine function, it will be run in the background loop together with other coroutines.
    Otherwise, it will be run in a separate thread.
    
    Args:
        func (Callable): The callable to run.
    
    Returns:
        Awaitable: The awaitable result of the callable. Can be cancelled if desired.
    """
    awaitable_func = None

    if asyncio.iscoroutinefunction(func):
        # If the callable is a coroutine function, run it in the background loop directly.
        awaitable_func = func()
    else:
        # If the callable is a normal function, run it in a separate thread.
        awaitable_func = asyncio.to_thread(func)

    return asyncio.run_coroutine_threadsafe(awaitable_func, get_background_loop())

def stop_background_loop():
    """Stops the background loop. Note that this does not cancel synchronous tasks."""
    if _background_loop.is_running():
        _background_loop.call_soon_threadsafe(_background_loop.stop)
