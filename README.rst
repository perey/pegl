==============================
Pegl: Python 3 binding for EGL
==============================

Pegl is a binding to EGL_, written in native Python 3 through the ctypes_
library. It provides comprehensive access to EGL_ functions, while offering a
Pythonic API.

EGL_ is a specification from the Khronos Group that provides an
intermediate layer between other Khronos specifications (OpenGL, OpenGL
ES, OpenVG), called "client APIs", and the native graphics system. EGL_
can supply an implicit rendering context for each of the client APIs,
as well as features like surfaces and buffering.

Pegl wraps EGL_ version 1.5, and is backwards compatible with previous versions
of the specification.

.. _EGL: http://www.khronos.org/egl
.. _ctypes: http://docs.python.org/py3k/library/ctypes

Roadmap
=======

The current Pegl version is 0.2a1. As an alpha version, care should be taken
before making use of the library!

----------
0.x series
----------

Releases in this series will provide a wrapper that is Pythonic, but still
fairly low-level, and the API is not guaranteed to be stable.

----------
1.x series
----------

Once the basic Pegl functionality is tested and considered usable, I will aim
to improve the API, so that an EGL environment can be set up with a minimum of
code. When I'm happy with the results, version numbers will be bumped up to
1.x, with a corresponding assurance of API stability.

License
=======

Pegl is free software, released under the `GNU GPLv3`_. See the file
``COPYING`` and individual source files for the full license terms.

.. _GNU GPLv3: http://www.gnu.org/licenses/gpl

Use
===
A typical use case might feature these steps:

1. Create a ``Display`` instance
2. Get a ``Config`` instance to match your requirements
3. Bind the client API you want to use
4. Get a ``Context`` instance and/or a ``Surface`` instance, as necessary
5. Do your work in the client API
6. Repeat from step 3 to mix different client APIs in the one application

Sample code for steps 1 to 4 might look like this:

>>> import pegl
>>> dpy = pegl.Display()
>>> conf = dpy.choose_config({pegl.ConfigAttrib.RENDERABLE_TYPE:
...                           pegl.ClientAPIFlag.OPENGL_ES})[0]
>>> pegl.bind_api(ClientAPI.OPENGL_ES)
>>> ctx = conf.get_context()
>>> surf = conf.create_pbuffer_surface({pegl.SurfaceAttrib.WIDTH: 640,
...                                     pegl.SurfaceAttrib.HEIGHT: 480})
>>> ctx.make_current(draw=surf)
