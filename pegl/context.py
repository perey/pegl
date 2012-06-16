#!/usr/bin/env python3

'''EGL context management.'''

# Copyright © 2012 Tim Pederick.
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

# Standard library imports.
from collections import namedtuple
from ctypes import c_int

# Local imports.
from . import make_int_p, native, NO_CONTEXT, NO_SURFACE
from .attribs import AttribList, NONE
from .attribs.context import ContextAttribs, ContextAPIs
from .config import get_configs
from .display import current_display

_api_lookup = lambda api: {ContextAPIs.OPENGL: 'OpenGL',
                           ContextAPIs.OPENGL_ES: 'OpenGL ES',
                           ContextAPIs.OPENVG: 'OpenVG',
                           NONE: None}.get(api, 'unknown')

def bind_api(api):
    '''Bind a client API to EGL in this thread.

    Keyword arguments:
        api -- The API to bind. This may be specified as a symbolic
            constant (OPENGL, OPENGL_ES, or OPENVG), or as a string
            naming one of those three APIs.

    '''
    if api not in ContextAPIs:
        # Try looking it up as a string label instead of a symbolic constant.
        guess_api = {'OPENGL': ContextAPIs.OPENGL,
                     'OPENGL_ES': ContextAPIs.OPENGL_ES,
                     'OPENVG': ContextAPIs.OPENVG,
                     }.get(str(api).upper().replace(' ', '_'))
        if guess_api is None:
            raise ValueError('not a valid API: {!r}'.format(api))
        else:
            api = guess_api
    native.eglBindAPI(api)

def bound_api(raw=False):
    '''Get the client API currently bound to EGL in this thread.

    Keyword arguments:
        raw -- If True, the integer value representing the API is
            returned as a hexadecimal string. If False or omitted,
            the name of the API is returned instead.
    Returns:
        A string, or None if no API is bound.

    '''
    api = native.eglQueryAPI()
    if api == NONE:
        return None
    elif raw:
        return hex(api)
    else:
        return _api_lookup(api)

def current_context():
    '''Get the current EGL context.'''
    ctxhandle = native.eglGetCurrentContext()
    if ctxhandle == NO_CONTEXT:
        return None
    else:
        return Context(ctxhandle=ctxhandle)

class Context:
    '''Represents an EGL context.

    Instance attributes:
        display -- The EGL display to which this context belongs; an
            instance of Display. This is set when the context is
            instantiated and is read-only thereafter.
        config -- The configuration that sets the parameters of this
            context; an instance of Config. This is set when the context
            is instantiated and is read-only thereafter.
        ctxhandle -- The foreign object handle for this context.
        api -- The client API for which this context was created.
        api_version -- The client API version specified when this
            context was created. This is only relevant for OpenGL ES
            contexts.
        render_buffer -- The buffer used by client API rendering, a
            value from RenderBufferTypes.

    '''
    def __init__(self, *args, **kwargs):
        '''Create the context.

        Keyword arguments:
            ctxhandle -- As the instance attribute. If this is supplied,
                no other arguments may be given.
            display -- As the instance attribute.
            config -- As the instance attribute.
            share_context -- An optional Context instance with which
                this context will share all resources that may be
                shared. If a context shares with more than one other
                context, all of those contexts will share the same
                resources.
            opengl_es_version -- Optionally specify the version of the
                OpenGL ES API to be supported. Only relevant when
                OpenGL ES is the current API, and optional even then;
                if omitted, EGL 1.4 specifies that OpenGL ES 1.x will
                be the default.

        '''
        # Which arguments have been supplied?
        if len(args) == 1:
            # Just the handle, as a positional argument.
            self._from_handle(args[0])
        elif len(kwargs) == 1 and 'ctxhandle' in kwargs:
            # Just the handle, as a keyword argument.
            self._from_handle(kwargs['ctxhandle'])
        else:
            # The full set of arguments, except maybe the optional ones.
            self._normal_init(*args, **kwargs)

    def _normal_init(self, display, config, share_context=None,
                     opengl_es_version=None):
        '''Create the context without a foreign object handle.

        Keyword arguments:
            display, config, share_context, opengl_es_version -- As the
                arguments to __init__().

        '''
        self.display = display
        self.config = config

        share_ctxhandle = (NO_CONTEXT if share_context is None else
                           share_context.ctxhandle)
        attribs = AttribList(attribs=ContextAttribs)
        if opengl_es_version is not None:
            attribs['CONTEXT_CLIENT_VERSION'] = opengl_es_version

        # Finally, create the context and save its handle.
        self.ctxhandle = native.eglCreateContext(self.display, self.config,
                                                 share_ctxhandle, attribs)

    def _from_handle(self, ctxhandle):
        '''Create the context from a foreign object handle.

        Keyword arguments:
            ctxhandle -- The foreign object handle to use.

        '''
        if ctxhandle == NO_CONTEXT:
            raise ValueError('cannot create a context using the null-context '
                             'handle')

        self.ctxhandle = ctxhandle
        # Since this call method is intended only for use by current_context(),
        # the display is going to be the current_display(). Or so one assumes.
        # FIXME: Race condition? The "current" display might have changed
        # between calls to current_context() and current_display()!
        self.display = current_display()

        # Safe to call _attr now that display and ctxhandle are set.
        config_id = self._attr(ContextAttribs.CONFIG_ID)
        self.config = get_configs(self.display,
                                  {ContextAttribs.CONFIG_ID: config_id})[0]

    def __del__(self):
        '''Delete the context object.'''
        native.eglDestroyContext(self.display, self)

    def __eq__(self, other):
        '''Compare two contexts for equivalence.

        Two contexts are considered equal if they have the same foreign
        function reference (i.e. the ctxhandle attribute).

        '''
        try:
            return self.ctxhandle == other.ctxhandle
        except AttributeError:
            # The other object doesn't have a ctxhandle.
            return False

    @property
    def _as_parameter_(self):
        '''Get the context reference for use by foreign functions.'''
        return self.ctxhandle

    def _attr(self, attr):
        '''Get the value of a context attribute.

        Keyword arguments:
            attr -- The identifier of the attribute requested.

        '''
        # Query the attribute, storing the result in a pointer.
        result = make_int_p()
        native.eglQueryContext(self.display, self, attr, result)

        # Dereference the pointer.
        return result.contents.value

    @property
    def api(self):
        '''Get the client API that this context supports.'''
        return _api_lookup(self._attr(ContextAttribs.CONTEXT_CLIENT_TYPE))

    @property
    def api_version(self):
        '''Get the client API version that this context supports.

        This value is presently only relevant for OpenGL ES contexts.

        '''
        return _api_lookup(self._attr(ContextAttribs.CONTEXT_CLIENT_VERSION))

    @property
    def render_buffer(self):
        '''Get the buffer used when rendering via this context.'''
        return self._attr(ContextAttribs.RENDER_BUFFER)

    def make_current(self, draw_surface=None, read_surface=None):
        '''Make this context the current one in this thread.

        Keyword arguments:
            draw_surface -- An optional surface object to make the
                current one for drawing operations.
            read_surface -- An optional surface object to make the
                current one for read operations. If read_surface is
                omitted and draw_surface is not, the same surface will
                be used for both.

        '''
        if draw_surface is None:
            draw_surface = NO_SURFACE
        if read_surface is None:
            read_surface = draw_surface
        native.eglMakeCurrent(self.display, draw_surface, read_surface, self)
