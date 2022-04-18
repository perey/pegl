==============
Sharing images
==============

.. py:module:: pegl.image

Despite the name, an EGL image is defined as a general-purpose object that can
be shared between client APIs. The specification says that it will “presumably”
be used for 2D image data, but this is in no way enforced!

The class listed below is defined in the :py:mod:`pegl.image` module, but is
also imported to the top-level :py:mod:`pegl` namespace.

The Image class
===============

.. py:class:: Image

    A data container (presumably 2D image data) that can be shared between
    client APIs. Users should not instantiate this class themselves, but should
    instead get instances from either
    :py:meth:`Display.create_image() <pegl.display.Display.create_image>` or from
    :py:meth:`Context.create_image() <pegl.context.Context.create_image>`.

    The EGL function underlying the destructor is :eglfunc:`eglDestroyImage`.

    .. availability:: EGL 1.5
