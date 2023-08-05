__all__ = ["LoggedClass", "LoggedFunction"]

import pylog2pdf


def LoggedClass(cls):
    class Wrapped(cls):
        def __init__(self, *args, **kwargs):
            mro = self.__class__.__mro__
            base_name = mro[-2].__name__
            if mro[0].__name__ == "Wrapped":
                cls_name = mro[1].__name__
            else:
                cls_name = mro[0].__name__
            pylog2pdf.LOG[base_name] = cls_name

            try:
                super().__init__(*args, **kwargs)
            except TypeError:
                pass

    return Wrapped


def LoggedFunction(func):
    def wrapped(*args, **kwargs):
        pylog2pdf.LOG["function"].append(func.__name__)
        return func(*args, **kwargs)

    return wrapped
