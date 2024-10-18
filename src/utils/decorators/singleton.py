from threading import Lock


def singleton(cls):
    """A singleton decorator, which makes sure that only one instance of a class exists."""
    instance = None
    lock = Lock()

    def get_instance(*args, **kwargs):
        """Get the instance of the class, or create a new one if it doesn't exist."""
        nonlocal instance

        # Check if a new instance should be created regardless of the existing one.
        if "force_new" in kwargs:
            force_new = kwargs.pop("force_new")

            if force_new:
                instance = None

        with lock:
            if not instance:
                instance = cls(*args, **kwargs)

        return instance

    return get_instance
