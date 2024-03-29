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
from util_test_common import needs_context, needs_display

# Import the module to be tested.
import pegl
from pegl import sync


@needs_context
class TestWaitFuncs(unittest.TestCase):
    """Test the wait functions provided by EGL."""
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


@unittest.skipIf(pegl.egl_version < (1, 5), 'EGL version too low')
@needs_context
class TestSyncCreation(unittest.TestCase):
    """Test creating a sync object from a display."""
    def test_create_fence_sync(self):
        """Try to create a fence sync object.

        This test passes if:

        - The create_sync method can be called with a sync type of
          pegl.SyncType.FENCE and no attributes
        - It returns a sync object
        - The sync object has a sync type of pegl.SyncType.FENCE

        """
        try:
            sync = self.dpy.create_sync(pegl.SyncType.FENCE)
        except pegl.BadMatchError:
            # There are three conditions under which creating a fence sync
            # object can result in a BadMatchError:
            # 1. The display used is not the current display
            self.assertIs(self.dpy, pegl.Display.get_current_display())
            # 2. There is no current context
            self.assertIsNot(pegl.Context.get_current_context(), None)
            # 3. The context does not support fence commands
            self.skipTest('context does not support fence commands')
        self.assertIsInstance(sync, pegl.sync.Sync)
        self.assertEqual(sync.sync_type, pegl.SyncType.FENCE)


if __name__ == '__main__':
    unittest.main(verbosity=2)
