# -*- coding: utf-8 -*-
"""
Provides abstract base classes for future use.
"""
# pylint: disable=abstract-class-instantiated
from .compat import *  # pylint: disable=wildcard-import, redefined-builtin
import abc


class ABC(with_metaclass(abc.ABCMeta, object)):
    """
    Analogous to python 3's abc.ABC
    """
    # pylint: disable=too-few-public-methods
    @classmethod
    def __subclasshook__(cls, C):
        return all(any(hasattr(cls_b, attr) for cls_b in C.__mro__)
                   for attr in cls.__abstractmethods__)


# You do NOT need to inherit from these classes to be it's subclass.
# All you need to do is implement all it's abstract methods.
class AbstractStructure(ABC):
    """
    Represents the conformation/structure of one or more molecules.

    Attributes
    ----------
    atoms : set/list/tuple/frozenset
        A collection of all atoms in this structure.
    residues : set/list/tuple/frozenset
        A collection of all residues (or molecules) in this structure.
    """
    @classmethod
    @abc.abstractmethod
    def from_file(cls, filename):
        """
        Parameters
        ==========
        filename : str
            A filename to read.
        Returns
        =======
        structure : Structure
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_text(cls, text):
        """
        Mainly intended for testing purposes.

        Parameters
        ==========
        text : str
            The text from which to construct a structure
        Returns
        =======
        structure : Structure
        """
        raise NotImplementedError

    @abc.abstractproperty
    def atoms(self):
        raise NotImplementedError

    @abc.abstractproperty
    def residues(self):
        raise NotImplementedError

    def __eq__(self, other):
        return id(self) == id(other)


class AbstractTrajectory(ABC):
    """
    Represents a time-series of Structures.
    """
    @abc.abstractmethod
    def __iter__(self):
        """
        Yields
        ------
        Structure
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __len__(self):
        """
        Returns
        -------
        length : int
            The number of frames in this trajectory.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, index):
        """
        Parameters
        ----------
        index : int

        Returns
        -------
        Structure
            The frame at index `index`
        """
        raise NotImplementedError

    def __eq__(self, other):
        return id(self) == id(other)


class AbstractAtom(ABC):
    """
    Represents an atom.

    Attributes
    ----------
    atom_type : AtomType
        The type of this atom.
    charge : float
        The charge of this atom.
    mass : float
        The mass of this atom.
    """
    def __init__(self, mass=None, charge=None):
        self.__mass = mass
        self.__charge = charge

    @abc.abstractproperty
    def atom_type(self):
        raise NotImplementedError

    @abc.abstractproperty
    def charge(self):
        if self.__charge is not None:
            return self.__charge
        else:
            return self.atom_type.charge

    @abc.abstractproperty
    def mass(self):
        if self.__mass is not None:
            return self.__mass
        else:
            return self.atom_type.mass

    def __eq__(self, other):
        return id(self) == id(other)


class AbstractAtomType(ABC):
    """
    Represents an atom type.

    Attributes
    ----------
    name : str
        The name of this atom type.
    charge : float
        The default charge for atoms of this type.
    mass : float
        The default mass for atoms of this type.
    """
    @abc.abstractproperty
    def name(self):
        raise NotImplementedError

    @abc.abstractproperty
    def charge(self):
        return 0

    @abc.abstractproperty
    def mass(self):
        return 0

    def __eq__(self, other):
        return id(self) == id(other)

    def __str__(self):
        return self.name
