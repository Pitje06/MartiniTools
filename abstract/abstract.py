# -*- coding: utf-8 -*-
"""
Provides abstract base classes for future use.
"""
# pylint: disable=abstract-class-instantiated
from ..compat import *  # pylint: disable=wildcard-import, redefined-builtin
import abc


class ABC(with_metaclass(abc.ABCMeta, object)):
    """
    Analogous to python 3's abc.ABC
    """
    # pylint: disable=too-few-public-methods
    @classmethod
    def __subclasshook__(cls, inspected_cls):
        return all(any(hasattr(cls_b, attr) for cls_b in inspected_cls.__mro__)
                   for attr in cls.__abstractmethods__)


# You do NOT need to inherit from these classes to be it's subclass.
# All you need to do is implement all it's abstract methods.
class AbstractStructure(ABC):
    """
    Represents the conformation/structure of one or more molecules.

    #TODO: Secondary Structure?

    Attributes
    ----------
    atoms : set/list/tuple/frozenset
        A collection of views on all atoms in this structure.
    residues : set/list/tuple/frozenset of Structures
        A collection of views on all residues (or molecules) in this structure.
    molecules : set/list/tuple/frozenset of Structures
        A collection of views on all molecules in this structure.
    chains : set/list/tuple/frozenset of Structures
        A collection of views on all chains (proteins, DNA, polymers) in this structures.
    """
    @classmethod
    @abc.abstractmethod
    def from_file(cls, filename, skip_hydrogens=False):
        """
        Parameters
        ----------
        filename : str
            A filename to read.
        skip_H : bool
            Whether hydrogen atoms should be skipped.
        Returns
        -------
        structure : Structure
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_text(cls, text, skip_hydrogens=False):
        """
        Mainly intended for testing purposes.

        Parameters
        ----------
        text : str
            The text from which to construct a structure
        skip_H : bool
            Whether hydrogen atoms should be skipped.
        Returns
        -------
        structure : Structure
        """
        raise NotImplementedError

    @abc.abstractproperty
    def atoms(self):
        raise NotImplementedError

    @abc.abstractproperty
    def residues(self):
        raise NotImplementedError

    @abc.abstractproperty
    def molecules(self):
        raise NotImplementedError

    @abc.abstractproperty
    def chains(self):
        raise NotImplementedError

    def __eq__(self, other):
        return id(self) == id(other)

    @abc.abstractmethod
    def __contains__(self, item):
        """
        Parameters
        ----------
        item : Structure
        Note
        ----
        On implementation, be wary of float rounding errors.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, selection):
        """
        e.g. protein['name CA']
        Parameters
        ----------
        selection : str or Selection
        """
        raise NotImplementedError


class AbstractTopology(ABC):
    """
    An topology

    Attributes
    ----------
    atoms
    bonded_interactions
    """


class AbstractInteraction(ABC):
    """
    An bonded or non-bonded interaction between atoms.

    Attributes
    ----------
    atoms
    parameters
    potential_function
    """
    @abc.abstractproperty
    def atoms(self):
        raise NotImplementedError

    @abc.abstractproperty
    def parameters(self):
        raise NotImplementedError

    @abc.abstractproperty  # Or method?
    def potential_function(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __repr__(self):
        raise NotImplementedError

    def __call__(self):
        """
        Evaluates potential_function between atoms.
        """
        return self.potential_function(self.atoms, self.parameters)


class AbstractMolecule(ABC, AbstractStructure, AbstractTopology):
    pass


class AbstractTrajectory(ABC):
    """
    Represents a time-series of Structures.
    Attributes
    ----------
    index : int
        The index of the current frame.
    time : float
        The time of the current frame in ps.
    frame : Structure
        The current frame.
    """
    @abc.abstractmethod
    def __iter__(self):
        """
        Yields
        ------
        Structure
        """
        raise NotImplementedError

    def __next__(self):
        """
        Increment self.time and self.frame
        """
        pass

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
        index : int or float
            If a float, index is considered as being a time, if an
            int, index is considered to be an index

        Returns
        -------
        Structure
            The frame at index `index`
        """
        raise NotImplementedError

    @abc.abstractproperty
    def index(self):
        raise NotImplementedError

    @index.setter
    def set_index(self, new_index):
        """
        Set the current index to new_index.
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


class AbstractSelection(ABC):
    """
    Something that can select part of a Structure
    """
    def __and__(self, other):
        raise NotImplementedError
    def __or__(self, other):
        raise NotImplementedError
    def __not__(self, other):
        raise NotImplementedError


class AbstractSystem(ABC, AbstractStructure, AbstractTopology):
    """
    Something something non-bonded interactions
    Non-bonded forcefield parameters
    Non-bonded functional forms
    Box, PBC
    lambda
    Propagator/Integrator. For version 3.
    """
    @abc.abstractmethod
    def distance(self, structure1, structure2, mode='com'):
        """
        Parameters
        ----------
        structure1 : Structure
        structure2 : Structure
        mode : str
            'com' : Determine the distance between the center of mass of
                    structure 1 and the center of mass of structure 2.
            'max' : ...
            'min' : ...

        Returns
        -------
        distance : float
            The Euclidean distance between structure 1 and structure 2,
            taking PBC into account.
        """
        raise NotImplementedError
