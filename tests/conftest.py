import pytest
from utils.background_loop import stop_background_loop


@pytest.hookimpl(tryfirst=True)
def pytest_unconfigure(config):
    """Hook called after the test session ends."""
    print("All tests have finished running, stopping background loop.")
    stop_background_loop()
