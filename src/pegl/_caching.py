#!/usr/bin/env python3

"""Instance caching for Pegl."""

# Copyright © 2020 Tim Pederick.
#
# This file is part of Pegl.
#
# Pegl is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pegl is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pegl. If not, see <http://www.gnu.org/licenses/>.

__all__ = ['Cached']

# Standard library imports.
from abc import ABC
import logging
from weakref import WeakValueDictionary

class Cached(ABC):
    """Cache instances of classes that implement this ABC.

    Instances must have an _as_parameter_ attribute, as used by ctypes.
    This must either be hashable itself, or have a value attribute that is
    hashable (as ctypes types do).

    """
    _cache = WeakValueDictionary()

    @classmethod
    def _add_to_cache(cls, instance):
        """Add an instance to the cache."""
        try:
            key = instance._as_parameter_.value
        except AttributeError:
            key = instance._as_parameter_

        cls._cache[key] = instance

    @classmethod
    def _remove_from_cache(cls, instance):
        """Remove an instance from the cache."""
        # TODO: Is this necessary? It's only (as far as I recall) called from
        # __del__ methods, but since the cache only holds weakrefs, its entries
        # will be deleted anyway when they're finalised, right?
        try:
            key = instance._as_parameter_.value
        except AttributeError:
            key = instance._as_parameter_

        del cls._cache[key]

    @classmethod
    def _new_or_existing(cls, key, *args, **kwargs):
        """Get a cached instance if it exists, or create a new one."""
        try:
            instance = cls._cache[key]
        except KeyError:
            logging.debug('Cache miss (%s): %r}', cls.__name__, key)
            instance = cls(*args, **kwargs)
        else:
            logging.debug('Cache hit (%s): %r}', cls.__name__, key)
        return instance
