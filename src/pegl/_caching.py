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
import logging
from weakref import WeakValueDictionary

def extract_key(key):
    """Ensure a key has a hashable value.

    The key must have a hashable attribute called value (as ctypes types
    do), or else it must itself be hashable. Note that hashability is not
    checked by this function; if it returns a non-hashable value, a
    TypeError will be raised when it is used to enter an instance into a
    mapping.

    """
    try:
        return key.value
    except AttributeError:
        return key

class Cached(type):
    """Metaclass for classes whose instances are cached.

    Two caches are used, both of which maintain weak references to their
    values, so as to not delay garbage collection when the caches hold the
    only references to the objects.

    The first cache tracks instances by the _as_parameter_ attribute, as
    used by ctypes. Instances must have such an attribute (or property),
    and it must either be hashable itself, or have a value attribute that
    is hashable (as ctypes types do).

    The second cache tracks instances by another property, _cache_key,
    defined by the class implementation, which must be hashable. This is
    included because there are EGL objects that can be uniquely identified
    in two ways:

    * Display objects can be identified by their handle (an EGLDisplay),
      or by the display_id argument used to create them (which must result
      in the same EGLDisplay handle being returned).
    * Config objects can be identified by their handle (an EGLConfig), or
      by the value of their config_id property.

    An instance will not be held in the second cache if its _cache_key is
    None; this is so that Display instances created without a display_id,
    and Context instances (which don't use the second cache), do not
    overwrite each other.

    """
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._param_cache = WeakValueDictionary()
        cls._prop_cache = WeakValueDictionary()

    def _add_to_cache(cls, instance):
        """Add an instance to the cache."""
        param_key = extract_key(instance._as_parameter_)

        cls._param_cache[param_key] = instance
        if instance._cache_key is not None:
            prop_key = extract_key(instance._cache_key)
            cls._prop_cache[prop_key] = instance
            logging.debug('Cached %s instance with param key %r, prop key %r',
                          cls.__name__, param_key, prop_key)
        else:
            logging.debug('Cached %s instance with param key %r',
                          cls.__name__, param_key)

    def _remove_from_cache(cls, instance):
        """Remove an instance from the cache."""
        # TODO: Is this necessary? It's only (as far as I recall) called from
        # __del__ methods, but since the cache only holds weakrefs, its entries
        # will be deleted anyway when they're finalised, right?
        param_key = extract_key(instance._as_parameter_)

        del cls._param_cache[param_key]
        if instance._cache_key is not None:
            prop_key = extract_key(instance._cache_key)
            del cls._prop_cache[prop_key]

    def _new_or_existing(cls, keys, *args, **kwargs):
        """Get a cached instance if it exists, or create a new one."""
        param_key, prop_key = keys

        instance = cls._param_cache.get(param_key)
        if instance is None:
            if prop_key is not None:
                instance = cls._prop_cache.get(prop_key)

            if instance is None:
                logging.debug('Cache miss (%s): %r}', cls.__name__, keys)
                instance = cls(*args, **kwargs)
            else:
                logging.debug('Prop cache hit (%s): %r}', cls.__name__,
                              prop_key)
        else:
            logging.debug('Param cache hit (%s): %r}', cls.__name__, param_key)
        return instance
