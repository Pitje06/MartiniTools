# -*- coding: utf-8 -*-
"""
Provides abstract base classes for future use.
"""
from compat import *

import abc


class ABC(with_metaclass(abc.ABCMeta, object)):
    """
    Analogous to python 3's abc.ABC
    """
    @classmethod
    def __subclasshook__(cls, C):
        return all(any(hasattr(B, attr) for B in C.__mro__)
                   for attr in cls.__abstractmethods__)


# You do NOT need to inherit from this class to be it's subclass.
# All you need to do is implement all it's abstract methods.
class Structure(ABC):
    @abc.abstractproperty
    def atoms(self):
        return None
