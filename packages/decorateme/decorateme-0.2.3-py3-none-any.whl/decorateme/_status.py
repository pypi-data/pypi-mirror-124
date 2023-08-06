"""
Decorators that warn about code maturity.
"""
import enum as _enum
from functools import wraps as _wraps
from typing import Union as _Union
from warnings import warn as _warn


class CodeIncompleteError(NotImplementedError):
    """The code is not finished!"""


class CodeWarning(UserWarning):
    """A warning related to code quality."""


class ObsoleteWarning(CodeWarning, PendingDeprecationWarning):
    """The code being called is obsolete and/or may be deprecated in the future."""


class DeprecatedWarning(CodeWarning, DeprecationWarning):
    """The code being called is deprecated."""


class ImmatureWarning(CodeWarning):
    """The code being called is unstable or immature."""


@_enum.unique
class CodeStatus(_enum.Enum):
    """
    An enum for the quality/maturity of code,
    ranging from incomplete to deprecated.
    """

    Incomplete = 0
    Immature = 1
    Preview = 2
    Stable = 3
    Obsolete = 4
    Deprecated = 5


def status(level: _Union[str, CodeStatus]):
    """
    Annotate code quality. Emits a warning if bad code is called.

    Args:
        level: The quality / maturity as an enum
    """

    if isinstance(level, str):
        level = CodeStatus[level.capitalize()]

    @_wraps(status)
    def dec(func):
        func.__status__ = level
        if level in [CodeStatus.Preview, CodeStatus.Stable]:
            return func
        elif level == CodeStatus.Incomplete:

            def my_fn(*args, **kwargs):
                raise CodeIncompleteError(str(func.__name__) + " is incomplete!")

            return _wraps(func)(my_fn)
        elif level == CodeStatus.Immature:

            def my_fn(*args, **kwargs):
                _warn(str(func.__name__) + " is immature", ImmatureWarning)
                return func(*args, **kwargs)

            return _wraps(func)(my_fn)
        elif level == CodeStatus.Obsolete:

            def my_fn(*args, **kwargs):
                _warn(str(func.__name__) + " is obsolete", ObsoleteWarning)
                return func(*args, **kwargs)

            return _wraps(func)(my_fn)
        elif level == CodeStatus.Deprecated:

            def my_fn(*args, **kwargs):
                _warn(str(func.__name__) + " is deprecated", DeprecatedWarning)
                return func(*args, **kwargs)

            return _wraps(func)(my_fn)
        raise AssertionError(f"What is {level}?")

    return dec
