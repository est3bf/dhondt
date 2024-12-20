class SingletonMeta(type):
    """
    Singleton metaclass.

    Usage::

        class MyClass(metaclass=Singleton):
            ...

    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
