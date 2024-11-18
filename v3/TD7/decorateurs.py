from functools import wraps

def singleton(orig_cls):
    orig_new = orig_cls.__new__
    instance = None

    @wraps(orig_cls.__new__)
    def __new__(cls):
        nonlocal instance
        if instance is None:
            instance = orig_new(cls)
        return instance
    orig_cls.__new__ = __new__
    return orig_cls
