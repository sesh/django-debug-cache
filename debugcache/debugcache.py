import sys
import types
import inspect

from time import strftime
from django.core.cache.backends.locmem import LocMemCache

try:
    from django.core.cache.backends.base import DEFAULT_TIMEOUT
except ImportError:
    DEFAULT_TIMEOUT = None


class DebugCacheMeta(type):
    """Wraps specific Django cache backend functions with some extra logging"""
    def __new__(cls, name, bases, attrs):
        for b in bases:
            for fn_name, fn in inspect.getmembers(b, predicate=inspect.ismethod):
                if fn_name in ['get', 'set', 'delete']:
                    setattr(b, fn_name, cls.logkey(fn))
        return super(DebugCacheMeta, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def logkey(cls, func):
        """Somewhat naively assumes that the key will be the first argument"""
        def fn(*args, **kwargs):
            sys.stdout.write("\n\033[93m[{}] CACHE {}: '{}'\033[0m".format(
               strftime("%d/%b/%Y %H:%M:%S"), func.func_name.upper(), args[1]))
            return func(*args, **kwargs)
        return fn


class DebugCache(LocMemCache):
    __metaclass__ = DebugCacheMeta
