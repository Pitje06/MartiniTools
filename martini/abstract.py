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
    """
    Represents the conformation/structure of one or more molecules.
    """
    @abc.abstractproperty
    def atoms(self):
        raise NotImplementedError
        return None

    @abc.abstractproperty
    def residues(self):
        raise NotImplementedError
        return []

    def __eq__(self, other):
        return id(self) == id(other)


class Trajectory(ABC):
    """
    Represents a time-series of Structures.
    """
    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __len__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, key):
        raise NotImplementedError

    def __eq__(self, other):
        return id(self) == id(other)


class Atom(ABC):
    """
    Represents an atom.
    """
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

    def __eq__(self, other):
        return id(self) == id(other)


class AtomType(ABC):
    """
    Represents an atom type.
    """
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

    def __eq__(self, other):
        return id(self) == id(other)

    def __str__(self):
        return self.name
