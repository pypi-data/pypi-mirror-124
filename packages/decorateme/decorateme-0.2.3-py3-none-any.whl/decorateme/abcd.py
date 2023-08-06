"""
A collection of decorators.
"""
from warnings import warn as _warn

_warn("abcd is deprecated; use 'import decorateme as abcd' instead", DeprecationWarning)

from decorateme import *
