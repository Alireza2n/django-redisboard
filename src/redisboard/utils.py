# shamelessly taken from kombu.utils
import sys

PY3 = sys.version_info[0] == 3


class LazySlicingIterable(object):
    def __init__(self, length_getter, items_getter):
        self.length_getter = length_getter
        self.items_getter = items_getter

    def __len__(self):
        return self.length_getter()

    def __getitem__(self, k):
        if isinstance(k, int):
            return self.items_getter(k, k)
        elif isinstance(k, slice):
            if k.step:
                raise RuntimeError("Can't use steps for slicing.")
            return self.items_getter(k.start, k.stop)
        else:
            raise TypeError("Must be int or slice.")


class cached_property(object):
    """Property descriptor that caches the return value
    of the get function.

    *Examples*

    .. code-block:: python

        @cached_property
        def connection(self):
            return Connection()

        @connection.setter  # Prepares stored value
        def connection(self, value):
            if value is None:
                raise TypeError("Connection must be a connection")
            return value

        @connection.deleter
        def connection(self, value):
            # Additional action to do at del(self.attr)
            if value is not None:
                print("Connection %r deleted" % (value, ))

    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.__get = fget
        self.__set = fset
        self.__del = fdel
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        try:
            return obj.__dict__[self.__name__]
        except KeyError:
            value = obj.__dict__[self.__name__] = self.__get(obj)
            return value

    def __set__(self, obj, value):
        if obj is None:
            return self
        if self.__set is not None:
            value = self.__set(obj, value)
        obj.__dict__[self.__name__] = value

    def __delete__(self, obj):
        if obj is None:
            return self
        try:
            value = obj.__dict__.pop(self.__name__)
        except KeyError:
            pass
        else:
            if self.__del is not None:
                self.__del(obj, value)

    def setter(self, fset):
        return self.__class__(self.__get, fset, self.__del)

    def deleter(self, fdel):
        return self.__class__(self.__get, self.__set, fdel)


# Straight from Django2's django.utils.functionl
# You can't trivially replace this with `functools.partial` because this binds
# to classes and returns bound instances, whereas functools.partial (on
# CPython) is a type and its instances don't bind.
def curry(_curried_func, *args, **kwargs):
    def _curried(*moreargs, **morekwargs):
        return _curried_func(*args, *moreargs, **{**kwargs, **morekwargs})

    return _curried
