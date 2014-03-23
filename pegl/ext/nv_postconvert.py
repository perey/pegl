#!/usr/bin/env python3

'''NVIDIA buffer-post conversion extension for EGL.

This extension defines behaviour when posting a colour buffer to a
destination buffer with lesser depth or fewer components.

http://www.khronos.org/registry/egl/extensions/NV/EGL_NV_post_convert_rounding.txt

The extension only defines behaviour for this situation; no new code is
required. Importing this module can serve as a check on whether posting
a mismatched buffer will cause an error or behave as per the extension.

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
