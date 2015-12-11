# -*- coding: utf-8 -*-
"""
An import and namespace 'manager' to facilitate
Python 2/3 compatibility.
Usage: from compat import *
"""
# pylint: disable=redefined-builtin, wildcard-import, unused-import, import-error

from __future__ import print_function, division
from __future__ import absolute_import, unicode_literals

import warnings
warnings.simplefilter('default')
import sys
import logging

# Version idempotent imports and corrections.
try:
    from six import with_metaclass
except ImportError:
    from future.utils import with_metaclass
from functools import reduce
from io import open
cmp = lambda x, y: (x > y) - (x < y)

# Version specific import and corrections
py_version = sys.version_info
if py_version[0] == 2:  # Major version
    # Require Python >2.7
    if py_version[1] < 7:  # Minor version
        raise EnvironmentError("Your Python version is too low, please upgrade.")
    else:
        logging.warn("You are running Python 2, but this is deprecated and may stop working...")
        from future_builtins import *
        input = raw_input  # pylint: disable=undefined-variable
        file = open

        def apply(func, args=(), kwargs={}):  # pylint: disable=unused-argument, dangerous-default-value
            """
            A function to discourage people from using apply.
            """
            raise NameError("name 'apply' is not defined")
# Require Python >3.4
elif py_version[0] == 3 and py_version[1] < 4:
    raise EnvironmentError("Your Python version is too low, please upgrade.")
