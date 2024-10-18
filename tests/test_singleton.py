# pylint: disable=E1123
from threading import Thread, current_thread
from utils.decorators.singleton import singleton


@singleton
class MySingleton:
    """A singleton class that only allows one instance to be created."""
    def __init__(self, name):
        self.name = name

# Test cases
def test_single_instance():
    """Test that multiple calls return the same instance."""
    # Act
    instance1 = MySingleton("Instance 1")
    instance2 = MySingleton("Instance 2")

    # Assert
    assert instance1 is instance2
    assert instance1.name == "Instance 1"
    assert instance2.name == "Instance 1"

def test_force_new_instance():
    """Test that force_new creates a new instance."""
    # Act
    instance1 = MySingleton("Instance 1")
    instance2 = MySingleton("Instance 2", force_new=True)

    # Assert
    assert instance1 is not instance2
    assert instance1.name == "Instance 1"
    assert instance2.name == "Instance 2"

def test_thread_safety():
    """Test that the singleton remains thread-safe."""
    # Arrange
    results = []

    def create_instance(name):
        instance = MySingleton(name)
        results.append((current_thread().name, instance))

    threads = [Thread(target=create_instance, args=(f"Thread-{i}",)) for i in range(10)]

    # Act
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Assert
    first_instance = results[0][1]
    for _, instance in results:
        assert instance is first_instance
