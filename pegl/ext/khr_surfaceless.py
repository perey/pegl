#!/usr/bin/env python3

'''Khronos surfaceless context extension for EGL.

This extension allows the current surface of a context to be None, in
order to render to a client API target without needing an EGL surface.

http://www.khronos.org/registry/egl/extensions/KHR/EGL_KHR_surfaceless_context.txt

The context module already allows the make_current() method of a Context
object to be called without a draw or read surface; any resulting EGL
error is simply propagated upwards. Importing this module can serve as a
check on whether that functionality will cause an error.

'''
# Copyright © 2013 Tim Pederick.
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

# No code! See docstring above.
