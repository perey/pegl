#!/usr/bin/env python3

"""EGL context management for Pegl."""

# Copyright © 2012, 2020 Tim Pederick.
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

from __future__ import annotations

__all__ = ['bind_api', 'query_api', 'Context']

# Standard library imports.
from typing import Any, Optional

# Local imports.
from . import egl
from ._caching import Cached
from .enums import ClientAPI, ReadOrDraw, RenderBuffer
from .errors import BadContextError
from .surface import Surface


# Inherit from type(Cached) to avoid metaclass conflicts.
class ContextMeta(type(Cached)):
    """Metaclass for EGL contexts, to enable class properties."""
    # Note that Context.get_current_surface is added to the class by the
    # pegl.display module, since its implementation needs the Display
    # class.
    @property
    def current_draw_surface(cls) -> Optional[Surface]:
        return cls.get_current_surface(ReadOrDraw.DRAW)

    @property
    def current_read_surface(cls) -> Optional[Surface]:
        return cls.get_current_surface(ReadOrDraw.READ)


class Context(Cached, metaclass=ContextMeta):
    """An EGL rendering context."""
    def __init__(self, display: Display, handle: Any):
        self._display = display
        self._as_parameter_ = handle

        self.__class__._add_to_cache(self)

    def __del__(self):
        # Remove this context from the cache.
        try:
            self.__class__._remove_from_cache(self)
        except AttributeError:
            # This instance never got its handle properly assigned.
            pass
        except KeyError:
            # This instance never got cached.
            pass

        # Destroy this context.
        try:
            egl.eglDestroyContext(self._display, self)
        except BadContextError:
            # This instance has an invalid handle, so there's nothing to
            # destroy.
            pass

    @classmethod
    def get_current_display(cls) -> Display:
        # Implemented in pegl.display to avoid dependency problems.
        raise NotImplementedError

    @classmethod
    def get_current_surface(cls, readdraw: ReadOrDraw) -> Optional[Surface]:
        # Implemented in pegl.display to avoid dependency problems.
        raise NotImplementedError

    @classmethod
    def release_current(cls) -> None:
        # Implemented in pegl.display to avoid dependency problems.
        raise NotImplementedError

    def make_current(self, draw: Optional[Surface]=None,
                     read: Optional[Surface]=None) -> None:
        """Make this context current for the calling thread.

        A single surface may be specified for both drawing and reading
        (which is compulsory for OpenVG contexts), or different surfaces
        may be specified for each. It is also possible to bind no surface
        for both—but not for just one of them. If only one surface is
        supplied, it will be bound for both drawing and reading.

        """
        if draw is None:
            if read is not None:
                draw = read
            else:
                draw = read = egl.EGL_NO_SURFACE
        elif read is None:
            read = draw

        egl.eglMakeCurrent(self._display, draw, read, self)

    @property
    def config(self) -> Config:
        # Implemented in pegl.config to avoid dependency problems.
        raise NotImplementedError

    @property
    def config_id(self) -> int:
        return egl.eglQueryContext(self._display, self, egl.EGL_CONFIG_ID)


if egl.egl_version >= (1, 2):
    def bind_api(api: ClientAPI) -> None:
        """Bind a client API as the current renderer in this thread."""
        egl.eglBindAPI(api)

    def query_api() -> Optional[ClientAPI]:
        """Get the client API that is bound for this thread."""
        api = ClientAPI(egl.eglQueryAPI())
        return (None if api == ClientAPI.NONE else api)

    __all__.extend(['bind_api', 'query_api'])

    def client_type(self) -> ClientAPI:
        return ClientAPI(egl.eglQueryContext(self._display, self,
                                             egl.EGL_CONTEXT_CLIENT_TYPE))
    Context.client_type = property(client_type)

    def render_buffer(self) -> Optional[RenderBuffer]:
        buffer = RenderBuffer(egl.eglQueryContext(self._display, self,
                                                  egl.EGL_RENDER_BUFFER))
        return (None if buffer == RenderBuffer.NONE else buffer)
    Context.render_buffer = property(render_buffer)


if egl.egl_version >= (1, 3):
    def client_version(self) -> int:
        return egl.eglQueryContext(self._display, self,
                                   egl.EGL_CONTEXT_CLIENT_VERSION)
    Context.client_version = property(client_version)
    # Alias for consistency with context creation, where as of EGL 1.5,
    # CLIENT_VERSION is renamed to MAJOR_VERSION and MINOR_VERSION is
    # provided alongside.
    Context.major_version = property(client_version)


if egl.egl_version >= (1, 4):
    def get_current_context(cls) -> Optional[Context]:
        # Implemented in pegl.display to avoid dependency problems.
        raise NotImplementedError
    Context.get_current_context = classmethod(get_current_context)


if egl.egl_version >= (1, 5):
    from .image import Image

    def create_image(self, target: ImageTarget, buffer, int,
                     attribs: Optional[dict[ImageAttrib, Any]]=None) -> Image:
        """Create an image from the given buffer."""
        return Image(self._display, egl.eglCreateImage(
                                        self._display, self, target, buffer,
                                        attrib_list(attribs, new_type=True)))
    Context.create_image = create_image
