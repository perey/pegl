==============
Sharing Images
==============

.. py:module:: pegl.image

This module provides the :py:class:`Image` class, instances of which represent
objects that can be shared between different client APIs. As the name suggests,
this is typically for images, but the specification is very non-specific in
this regard, only saying that it will "presumably" be 2D image data.

This module is only available on EGL 1.5.

Images
======

.. py:class:: Image

    An image represents state (presumably 2D image data) that can be shared
    between multiple client APIs. Users should not instantiate this class
    themselves, but should instead get instances from the
    :py:meth:`Display.create_image` or :py:meth:`Context.create_image` method.

    The EGL function underlying the destructor is ``eglDestroyImage``.

.. py:class:: ImageAttrib

    An enumeration of image attributes.

    - GL_TEXTURE_LEVEL
    - GL_TEXTURE_ZOFFSET
    - IMAGE_PRESERVED

.. py:class:: ImageTarget

    An enumeration of image targets.

    - GL_TEXTURE_2D
    - GL_TEXTURE_CUBE_MAP_POSITIVE_X
    - GL_TEXTURE_CUBE_MAP_NEGATIVE_X
    - GL_TEXTURE_CUBE_MAP_POSITIVE_Y
    - GL_TEXTURE_CUBE_MAP_NEGATIVE_Y
    - GL_TEXTURE_CUBE_MAP_POSITIVE_Z
    - GL_TEXTURE_CUBE_MAP_NEGATIVE_Z
    - GL_TEXTURE_3D
    - GL_RENDERBUFFER