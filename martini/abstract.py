# -*- coding: utf-8 -*-
"""
Provides abstract base classes for future use.
"""
from .compat import *
import abc


class ABC(with_metaclass(abc.ABCMeta, object)):
    """
    Analogous to python 3's abc.ABC
    """
    @classmethod
    def __subclasshook__(cls, C):
        return all(any(hasattr(B, attr) for B in C.__mro__)
                   for attr in cls.__abstractmethods__)


# You do NOT need to inherit from these classes to be it's subclass.
# All you need to do is implement all it's abstract methods.
class Structure(ABC):
    @abc.abstractproperty
    def atoms(self):
        return None

    @abc.abstractproperty
    def residues(self):
        return []


class Trajectory(ABC):
    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __len__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, key):
        raise NotImplementedError


class Atom(ABC):
    @abc.abstractproperty
    def atom_type(self):
        raise NotImplementedError
        return None

    @abc.abstractproperty
    def charge(self):
        raise NotImplementedError
        return self.atom_type.charge

    @abc.abstractproperty
    def mass(self):
        raise NotImplementedError
        return self.atom_type.mass


class AtomType(ABC):
    @abc.abstractproperty
    def name(self):
        raise NotImplementedError
        return ''

    @abc.abstractproperty
    def charge(self):
        raise NotImplementedError
        return 0

    @abc.abstractproperty
    def mass(self):
        raise NotImplementedError
        return 0

    def __str__(self):
        return self.name
