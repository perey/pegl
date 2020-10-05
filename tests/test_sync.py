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


class TestWaitFuncs(unittest.TestCase):
    """Test the wait functions provided by EGL."""
    def setUp(self):
        """Set up a display and context for testing."""
        if pegl.egl_version < (1, 4):
            self.dpy = pegl.display.Display(get_native_display())
        else:
            self.dpy = pegl.display.Display()
        self.cfg = self.dpy.get_configs(1)[0]
        self.ctx = self.cfg.create_context()
        self.surf = self.cfg.create_pbuffer_surface()
        self.ctx.make_current(self.surf)

    @unittest.skipIf(pegl.egl_version < (1, 2), 'EGL version too low')
    def test_wait_client(self):
        """Try telling native rendering to wait on client API rendering.

        This test passes if:

        - wait_client can be called
        - Its return value is None

        """
        result = sync.wait_client()
        self.assertIs(result, None)

    def test_wait_gl(self):
        """Try telling native rendering to wait on OpenGL ES rendering.

        This test passes if:

        - wait_gl can be called
        - Its return value is None

        """
        result = sync.wait_gl()
        self.assertIs(result, None)

    def test_wait_native(self):
        """Try telling client API rendering to wait on native rendering.

        This test passes if:

        - wait_native can be called with no argument
        - Its return value is None

        """
        result = sync.wait_native()
        self.assertIs(result, None)

    def test_wait_native_engine(self):
        """Try telling client API rendering to wait on native rendering.

        This test passes if:

        - wait_native can be called with each native engine defined in the
          NativeEngine enumeration
        - Its return value is None in each case

        """
        for n, engine in enumerate(pegl.NativeEngine):
            with self.subTest(msg=engine, n=n):
                result = sync.wait_native(engine)
                self.assertIs(result, None)

    def tearDown(self):
        """Finalize EGL objects created for testing."""
        pegl.Context.release_current()
        del self.surf
        del self.ctx
        del self.dpy


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
