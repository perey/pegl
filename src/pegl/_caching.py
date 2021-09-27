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

__all__ = ['cached']

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

def cached(*cache_keys):
    """Construct a decorator for classes whose instances are cached.

    Multiple caches may be used, each of which maintains weak references
    to their values, so as to not delay garbage collection when the caches
    hold the only references to the objects.

    For all Pegl uses, the first cache will be keyed by the _as_parameter_
    attribute, as used by ctypes. Instances must have such an attribute
    (or property), and it must either be hashable itself, or have a value
    attribute that is hashable (as ctypes types do).

    A second cache is used for Display objects (caching them by the
    display_id argument used to create them) and for Config objects
    (caching them by their config_id property).

    A key that is None will not be used to cache any instance (but a key
    that has a value attribute of None can be). When looking up cached
    instances, each cache is searched in order (again skipping any keys
    that are None) until a match is found or all caches have been tried.

    """
    def cached_class(cls):
        cls._cache_keys = cache_keys
        cls._caches = [WeakValueDictionary() for _ in cache_keys]

        def _add_to_cache(cls, instance):
            """Add an instance to the cache."""
            used_keys = [] # For debugging only.
            for keyname, cache in zip(cls._cache_keys, cls._caches):
                raw_key = getattr(instance, keyname)
                key = extract_key(raw_key)
                used_keys.append(raw_key)

                if raw_key is not None:
                    cache[key] = instance

            logging.debug('Cached %s instance with keys %r',
                          cls.__name__, used_keys)
        setattr(cls, '_add_to_cache', classmethod(_add_to_cache))

        def _remove_from_cache(cls, instance):
            """Remove an instance from the cache."""
            # TODO: Is this necessary? It's only (as far as I recall) called
            # from __del__ methods, but since the cache only holds weakrefs,
            # its entries will be deleted anyway when they're finalised, right?
            for keyname, cache in zip(cls._cache_keys, cls._caches):
                raw_key = getattr(instance, keyname)
                key = extract_key(raw_key)
                if raw_key is not None:
                    del cache[key]
        setattr(cls, '_remove_from_cache', classmethod(_remove_from_cache))

        def _get_existing(cls, keys):
            """Get a cached instance if it exists, or else None."""
            for key, keyname, cache in zip(keys, cls._cache_keys, cls._caches):
                if key is None:
                    continue

                instance = cache.get(extract_key(key))
                if instance is not None:
                    logging.debug('Cache hit (%s, %r): %r', cls.__name__,
                                  keyname, key)
                    return instance

            logging.debug('Cache miss (%s): %r', cls.__name__, keys)
            return None
        setattr(cls, '_get_existing', classmethod(_get_existing))

        def _new_or_existing(cls, keys, *args, **kwargs):
            """Get a cached instance if it exists, or create a new one."""
            instance = cls._get_existing(keys)

            return (instance if instance is not None else cls(*args, **kwargs))
        setattr(cls, '_new_or_existing', classmethod(_new_or_existing))

        return cls

    return cached_class
