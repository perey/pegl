#!/usr/bin/env python3

'''Cross-vendor extension type extension for EGL.

This extension extends the existing extension-loading mechanism (which
requires a Display instance) by allowing extensions to be queried and
loaded before a Display is set up. Specifically, extensions are now
divided into "display extensions" (loaded in the existing way) and
"client extensions" (loaded without a Display).

As such, this module (unlike other extensions) should be imported
directly. Its load_extension() function can then be used to import
modules for client extensions.

http://www.khronos.org/registry/egl/extensions/EXT/EGL_EXT_client_extensions.txt

'''
# Copyright © 2014 Tim Pederick.
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

# Local imports.
from .. import native, BadDisplayError
from ..display import EXTENSIONS

# Keep this extension's name string handy.
NAME_STRING = 'EGL_EXT_client_extensions'

# Attempt to load the extensions string. If this raises a BadDisplayError, the
# extension for this module is not supported by the EGL implementation.
try:
    client_extensions = tuple(native.eglQueryString(None, EXTENSIONS).
                              decode('ISO-8859-1').split())
except BadDisplayError:
    # Extension not supported.
    raise ImportError("extension '{}' is not supported".format(NAME_STRING))
# We should also check to make sure that this extension is explicitly listed
# in the results. Any other exceptions will be allowed to propagate upwards.
if NAME_STRING not in client_extensions:
    raise ImportError("extensions queried successfully, but '{}' support not "
                      "declared".format(NAME_STRING))

# New extension loader.
def load_extension(extname):
    '''Load an extension conditional on it being declared available.

    The client_extensions attribute of this module is used to determine
    whether the extension named is supported by this implementation of
    EGL. An ImportError will be raised to signify that the extension is
    unavailable. Also, even when it is declared to be available, if an
    ImportError occurs anyway while the extension module is being
    loaded, it will be raised.

    Keyword arguments:
        extname -- The name string of the extension. Name strings
            are consistently of the form EGL_xxx_yyy, where xxx
            represents the vendor proposing the extension (or EXT
            for a cross-vendor proposal) and yyy is a descriptive
            name for the extension.

    '''
    # Ensure the name is a string.
    extname = str(extname)

    if extname not in client_extensions:
        raise ImportError("extension '{}' unsupported or not a client "
                          "extension".format(extname))

    # What module has this extension?
    from . import extensions as extlist
    module_name = extlist.get(extname)

    if module_name is None:
        raise ImportError("no module found for extension "
                          "'{}'".format(extname))
    else:
        pkg_with_module = __import__(vendor_pkg, globals(), locals(),
                                     [module_name], 1)
        return getattr(pkg_with_module, module_name)
