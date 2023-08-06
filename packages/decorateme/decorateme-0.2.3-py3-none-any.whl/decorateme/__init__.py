"""
Metadata for decorateme.
"""

import logging
from importlib.metadata import PackageNotFoundError
from importlib.metadata import metadata as __load
from pathlib import Path

from decorateme.abcd import *

pkg = Path(__file__).absolute().parent.name
logger = logging.getLogger(pkg)
metadata = None
try:
    metadata = __load(Path(__file__).absolute().parent.name)
    __status__ = "Development"
    __copyright__ = "Copyright 2017–2021"
    __date__ = "2020-08-24"
    __uri__ = metadata["home-page"]
    __title__ = metadata["name"]
    __summary__ = metadata["summary"]
    __license__ = metadata["license"]
    __version__ = metadata["version"]
    __author__ = metadata["author"]
    __maintainer__ = metadata["maintainer"]
    __contact__ = metadata["maintainer"]
except PackageNotFoundError:  # pragma: no cover
    logger.error(f"Could not load package metadata for {pkg}. Is it installed?")

from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass
from functools import total_ordering
from typing import final

from decorateme._auto import (
    auto_eq,
    auto_hash,
    auto_html,
    auto_info,
    auto_obj,
    auto_repr,
    auto_repr_str,
    auto_str,
    auto_utils,
)
from decorateme._behavior import (
    auto_singleton,
    auto_timeout,
    immutable,
    mutable,
    takes_seconds,
    takes_seconds_named,
)
from decorateme._doc import append_docstring, copy_docstring
from decorateme._informative import (
    external,
    internal,
    not_thread_safe,
    override_recommended,
    overrides,
    reserved,
    thread_safe,
)
from decorateme._over import (
    collection_over,
    float_type,
    int_type,
    iterable_over,
    sequence_over,
)
from decorateme._status import (
    CodeIncompleteError,
    CodeStatus,
    CodeWarning,
    DeprecatedWarning,
    ImmatureWarning,
    ObsoleteWarning,
    status,
)

__all__ = [
    "ABC",
    "ABCMeta",
    "CodeIncompleteError",
    "CodeStatus",
    "CodeWarning",
    "DeprecatedWarning",
    "ImmatureWarning",
    "ObsoleteWarning",
    "abstractmethod",
    "append_docstring",
    "auto_eq",
    "auto_hash",
    "auto_html",
    "auto_info",
    "auto_obj",
    "auto_repr",
    "auto_repr_str",
    "auto_singleton",
    "auto_str",
    "auto_timeout",
    "collection_over",
    "copy_docstring",
    "dataclass",
    "external",
    "final",
    "float_type",
    "immutable",
    "int_type",
    "internal",
    "iterable_over",
    "mutable",
    "not_thread_safe",
    "override_recommended",
    "overrides",
    "reserved",
    "sequence_over",
    "takes_seconds",
    "takes_seconds_named",
    "thread_safe",
    "total_ordering",
    "auto_utils",
]
