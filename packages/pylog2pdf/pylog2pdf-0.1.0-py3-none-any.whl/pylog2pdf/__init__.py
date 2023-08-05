# flake8: noqa

try:
    from importlib_metadata import version
except ImportError:
    from importlib.metadata import version  # Python 3.8+

try:
    __version__ = version("pylog2pdf")
except:
    __version__ = ""


class GlobalDict(dict):
    _instance = None

    def __new__(cls, *args, **kwargs) -> "GlobalDict":
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


LOG = GlobalDict()
LOG.update({"function": []})

from .logger import *
from .pdf_io import *
