import pytest
from utils.background_loop import stop_background_loop


@pytest.hookimpl(tryfirst=True)
def pytest_unconfigure():
    """Hook called after the test session ends."""
    print("All tests have finished running, stopping background loop.")
    stop_background_loop()

def pytest_collection_modifyitems(items):
    """Modify the items collection before running the tests."""
    for item in items:
        item.add_marker(pytest.mark.httpx_mock(assert_all_responses_were_requested=False))
