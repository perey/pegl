#!/usr/bin/env python3

'''ARM multisample discarding extension for EGL.

This extension allows the multisample buffer of pixmap surface to be
marked as discardable. This is aimed at GPU hardware that does all
multisampled rendering internally and only writes downsampled data to
external memory, thus making the EGL multisample buffer redundant.

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

# Local imports.
from ..attribs.surface import SurfaceAttribs
from ..surface import PixmapSurface

# New surface attribute.
SurfaceAttribs.extend('DISCARD_SAMPLES', 0x3286, bool, False)

# Allow querying the new attribute on pixmap surfaces.
def samples_discardable(self):
    '''Determine whether the multisample buffer is discardable.'''
    return self._attr(SurfaceAttribs.DISCARD_SAMPLES)
PixmapSurface.samples_discardable = property(samples_discardable)
