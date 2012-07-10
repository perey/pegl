==============================
Pegl: Python 3 binding for EGL
==============================

Pegl is a binding to EGL_ 1.4, written in native Python 3 through the
ctypes_ library. It provides comprehensive access to EGL_ functions,
while offering a very Pythonic API.

EGL_ is a specification from the Khronos Group that provides an
intermediate layer between other Khronos specifications (OpenGL, OpenGL
ES, OpenVG), called "client APIs", and the native graphics system. EGL_
can supply an implicit rendering context for each of the client APIs,
as well as features like surfaces and buffering.

Pegl wraps EGL_ version 1.4. It is unlikely to be backwards compatible
with previous versions of the specification.

.. _EGL: http://www.khronos.org/egl
.. _ctypes: http://docs.python.org/py3k/library/ctypes

Roadmap
=======

The current Pegl version is 0.1a3~1.4. As an alpha version, care should
be taken before making use of the library; it wraps the complete EGL API
and all intended extensions, but it is very much untested.

Pegl version numbers are in this format:

    ``w.x~y.z``

where ``w.x`` represents the major/minor Pegl release (including alpha,
beta or release candidate status, if appropriate), and ``y.z`` represents
the EGL version being wrapped.

----------
0.x series
----------

Releases in this series will provide a wrapper that is Pythonic, but
still fairly low-level, and the API is not guaranteed to be stable.

----------
1.x series
----------

Once the basic Pegl functionality is tested and considered usable, I
will aim to improve the API, so that an EGL environment can be set up
with a minimum of code. When I'm happy with the results, version
numbers will be bumped up to 1.x, and some assurance of API stability
will be given.

License
=======

Pegl is free software, released under the `GNU GPLv3`_. See the file
``COPYING`` and individual source files for the full license terms.

.. _GNU GPLv3: http://www.gnu.org/licenses/gpl

Use
===
A typical use case might feature these steps:

1. Create a ``Display`` instance (`pegl.display`_).
2. Import whatever attribute objects (`pegl.attribs`_) you need to
   express your requirements
3. Get a ``Config`` instance (`pegl.config`_) to match your
   requirements.
4. Bind the client API you want to use (`pegl.context`_).
5. Get a ``Context`` instance (`pegl.context`_) and/or a ``Surface``
   instance (`pegl.surface`_), as necessary.
6. Do your work in the client API.
7. Repeat from step 4 to mix different client APIs in the one
   application.

Sample code for steps 1 to 5 might look like this:

>>> import pegl
>>> from pegl.attribs.config import ClientAPIs, CBufferTypes
>>> from pegl.attribs.context import ContextAPIs
>>> dpy = pegl.display.Display()
>>> conf = pegl.config.get_configs(dpy,
...                                {'RENDERABLE_TYPE': ClientAPIs(OPENVG=1),
...                                 'COLOR_BUFFER_TYPE': CBufferTypes.RGB})[0]
>>> pegl.context.bind_api(ContextAPIs.OPENVG)
>>> ctx = pegl.context.Context(dpy, conf)
>>> surf = pegl.surface.PbufferSurface(dpy, conf, {'WIDTH': 640,
...                                                'HEIGHT': 480})
>>> ctx.make_current(draw_surface=surf)

The Library
===========
The main Pegl package, ``pegl``, contains six modules and two
subpackages. The top-level package namespace also holds all exception
types, plus a few constants and utility functions.

------------
pegl.attribs
------------
The ``attribs`` subpackage divides the many EGL attributes into modules
according to the object type to which they apply. These modules contain
various named tuples and classes, providing namespaces by which the
attributes are grouped and given symbolic names. Import the ones you
need, as you need them.

-----------
pegl.config
-----------
The ``config`` module revolves around the ``Config`` class, which
represents a set of EGL configuration options. You will want to obtain
a Config that matches your application requirements (color depth, APIs
supported, etc.) by calling ``get_configs()`` and using one of the
configurations it returns. EGL sorts the configurations so that you
will usually get the best match by choosing the first result.

------------
pegl.context
------------
The ``context`` module chiefly features the ``Context`` class and the
functions ``bind_api()`` and ``bound_api()``. Once you have a
configuration, you will usually want to bind an API and then create a
``Context`` instance with your ``Display`` and ``Config``.

------------
pegl.display
------------
An EGL display is not merely a representation of a physical screen; it
is the basic environment of all EGL operations, and holds details of the
EGL implementation itself. The ``display`` module has a ``Display``
class that handles all of these functions. Creating a ``Display``
instance will usually be the first step when using EGL.

--------
pegl.ext
--------
A large selection of EGL extensions are given wrappers in the ``ext``
subpackage, sorted into further subpackages by vendor. Cross-vendor
("EXT") extensions live in the main ``ext`` subpackage.

All extensions in the EGL Registry as of June 2012 are supported,
except for the following:

+-----+----------------------------------+--------------------------------+
|Ext #|           Name string            |             Reason             |
+=====+==================================+================================+
|1    |``EGL_KHR_config_attribs``        |Now part of core EGL.           |
+-----+----------------------------------+--------------------------------+
|17   |``EGL_NV_coverage_sample``        |NVIDIA proprietary.             |
+-----+----------------------------------+                                |
|18   |``EGL_NV_depth_nonlinear``        |                                |
+-----+----------------------------------+--------------------------------+
|24   |``EGL_HI_clientpixmap``           |Underspecified; specifically,   |
|     |                                  |``EGL_CLIENT_PIXMAP_POINTER_HI``|
|     |                                  |is undefined.                   |
+-----+----------------------------------+--------------------------------+
|25   |``EGL_HI_colorformats``           |Seems pointless without the     |
|     |                                  |above. Also, its enum values are|
|     |                                  |missing from ``eglenum.spec``.  |
+-----+----------------------------------+--------------------------------+
|30   |``EGL_NV_coverage_sample_resolve``|NVIDIA proprietary.             |
+-----+----------------------------------+--------------------------------+

In addition, some extensions that are not officially registered, but are
widely available through the Mesa library, are supported by Pegl:

* ``EGL_NOK_swap_region``
* ``EGL_WL_bind_wayland_display``

-----------
pegl.native
-----------
The ``native`` module provides the wrapper around the functions in the
native EGL library, as well as error checking wrapped around them. It is
generally not necessary to access this module in your own applications.

------------
pegl.surface
------------
The ``surface`` module has classes for the different types of rendering
surface that EGL supports: on-screen surfaces bound to native windows
(``WindowSurface``), off-screen surfaces bound to pixel buffers
(``PbufferSurface``), and surfaces that render to native pixmap objects
(``PixmapSurface``).

---------
pegl.sync
---------
The ``sync`` module wraps the small number of core EGL synchronization
functions that help ensure that native and client rendering calls do not
interfere with one another. More advanced synchronization features are
available in extensions_ (``pegl.ext.khr.sync``, ``pegl.ext.nv.sync``).

.. _extensions: `pegl.ext`_
