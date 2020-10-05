#!/usr/bin/env python3

'''Unit tests for the pegl.sync module.'''

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

# Standard library imports.
import unittest

# Import test utilities.
from util_test_display import get_native_display

# Import the module to be tested.
import pegl
from pegl import sync


@unittest.skipIf(pegl.egl_version < (1, 5), 'EGL version too low')
class TestSyncCreation(unittest.TestCase):
    """Test creating a sync object from a display."""
    def setUp(self):
        """Set up a display for testing."""
        if pegl.egl_version < (1, 4):
            self.dpy = pegl.display.Display(get_native_display())
        else:
            self.dpy = pegl.display.Display()

    @unittest.skip('The sync handle supplied is invalid and cannot be queried,'
                   ' plus this has weird side effects where other tests start '
                   'to fail.')
    def test_create_fence_sync(self):
        """Try to create a fence sync object.

        This test passes if:

        - The create_sync method can be called with a sync type of
          pegl.SyncType.FENCE and no attributes
        - It returns a sync object
        - The sync object has a sync type of pegl.SyncType.FENCE

        """
        sync = self.dpy.create_sync(pegl.SyncType.FENCE)
        self.assertIsInstance(sync, pegl.sync.Sync)
        self.assertEqual(sync.sync_type, pegl.SyncType.FENCE)


if __name__ == '__main__':
    unittest.main(verbosity=2)
