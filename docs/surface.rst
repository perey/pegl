==================
Rendering Surfaces
==================

.. py:module:: pegl.surface

This module provides the :py:class:`Surface` class. Instances of this class,
which are obtained from :py:class:`Config` instances, represent a target to
which graphics can be rendered, whether on-screen or in memory.

Surfaces
========

.. py:class:: Surface

    A surface represents a target to which graphics can be rendered. Users
    should not instantiate this class themselves, but should instead get an
    instance from the relevant :py:class:`Config` method (one of
    :py:meth:`Config.create_pbuffer_surface`,
    :py:meth:`Config.create_pbuffer_surface_from_client_buffer`,
    :py:meth:`Config.create_pixmap_surface`,
    :py:meth:`Config.create_platform_pixmap_surface`,
    :py:meth:`Config.create_platform_window_surface`, and
    :py:meth:`Config.create_window_surface`).

    Instances of this class are cached until their destructor is called, so
    that they can be retrieved by the :py:meth:`Context.draw_surface` and
    :py:meth:`Context.read_surface` properties.

    The EGL function underlying the destructor is ``eglDestroySurface``.

    .. py:method:: bind_tex_image(buffer: RenderBuffer=RenderBuffer.BACK)
                       -> None

        Bind the given buffer of this (pbuffer) surface as a texture. Note that
        only :py:obj:`RenderBuffer.BACK` is allowed, even for a single-buffered
        surface, as it indicates the buffer into which rendering is taking
        place. As such, the ``buffer`` argument may be omitted.

        The underlying EGL function is ``eglBindTexImage``.

    .. py:method:: release_tex_image(buffer: RenderBuffer=RenderBuffer.BACK)
                       -> None

        Release the given buffer of this (pbuffer) surface from its binding as
        a texture. Note that only :py:obj:`RenderBuffer.BACK` is allowed, even
        for a single-buffered surface, as it indicates the buffer into which
        rendering is taking place. As such, the ``buffer`` argument may be
        omitted.

        While this method undoes the effect of :py:meth:`bind_tex_image`, it is
        not an error to call it when the buffer is not actually bound.

        The underlying EGL function is ``eglReleaseTexImage``.

    .. py:method:: copy_buffers(target: int) -> None

        Copy the colour buffer of this surface to a native pixmap. The
        ``target`` argument is a platform-specific native pixmap object (a
        ``Pixmap`` on X11, a ``HBITMAP`` on Windows, etc.), handled as a
        ``void *`` in C and as an ``int`` in Python.

        The underlying EGL function is ``eglCopyBuffers``.

    .. py:method:: swap_buffers() -> None

        Post the back colour buffer of this (window) surface to the window.
        This method has no effect on pbuffer or pixmap surfaces, nor on
        single-buffered window surfaces.

        The underlying EGL function is ``eglSwapBuffers``.

    .. py:method:: config_id -> int

        :property:

        A read-only property that retrieves the unique identifier of the
        configuration used to create this surface.

        The underlying EGL function is ``eglQuerySurface`` with an
        ``attribute`` value of ``EGL_CONFIG_ID``.

    .. py:method:: height -> int

        :property:

        A read-only property that gets the height, in pixels, of this surface,
        as most recently registered by the EGL implementation (which may not
        immediately reflect resizing operations from the platform).

        The underlying EGL function is ``eglQuerySurface`` with an
        ``attribute`` value of ``EGL_HEIGHT``.

    .. py:method:: horizontal_resolution -> Optional[float]

        :property:

        A read-only property that gets the horizontal resolution of the display
        on which this (window) surface is visible, in pixels per metre. For a
        non-window surface, the result is None.

        The underlying EGL function is ``eglQuerySurface`` with an
        ``attribute`` value of ``EGL_HORIZONTAL_RESOLUTION``. The given value
        is scaled by dividing by the value of ``EGL_DISPLAY_SCALING`` (which is
        defined to be 10000).

    .. py:method:: largest_pbuffer -> bool

        :property:

        A read-only property that checks whether, when this (pbuffer) surface'
        was created, the EGL implementation was allowed to return the largest
        available pbuffer if the requested pbuffer could not be created. This
        is always False for non-pbuffer surfaces.

        The underlying EGL function is ``eglQuerySurface`` with an
        ``attribute`` value of ``EGL_LARGEST_PBUFFER``.

    .. py:method:: pixel_aspect_ratio -> Optional[float]

        :property:

        A read-only property that gets the pixel aspect ratio of the display
        on which this (window) surface is visible, as width divided by height.
        For a non-window surface, the result is None.

        The underlying EGL function is ``eglQuerySurface`` with an
        ``attribute`` value of ``EGL_PIXEL_ASPECT_RATIO``. The given value
        is scaled by dividing by the value of ``EGL_DISPLAY_SCALING`` (which is
        defined to be 10000).

    .. py:method:: mipmap_level -> int

        :property:

        A property specifying which level of the OpenGL ES mipmap texture
        should be rendered.

        The EGL function underlying the getter is ``eglQuerySurface``, while
        the setter calls ``eglSurfaceAttrib``. Each is called with an
        ``attribute`` value of ``EGL_MIPMAP_LEVEL``.

    .. py:method:: mipmap_texture -> bool

        :property:

        A read-only property that checks whether or not storage should be
        allocated for OpenGL ES mipmaps.

        The underlying EGL function is ``eglQuerySurface`` with an
        ``attribute`` value of ``EGL_MIPMAP_TEXTURE``.

    .. py:method:: multisample_resolve -> MultisampleResolve

        :property:

        A property specifying the filter method for resolving the multisample
        buffer.

        The EGL function underlying the getter is ``eglQuerySurface``, while
        the setter calls ``eglSurfaceAttrib``. Each is called with an
        ``attribute`` value of ``EGL_MULTISAMPLE_RESOLVE``.

    .. py:method:: render_buffer -> RenderBuffer

        :property:

        A read-only property specifying which buffer client APIs are requested
        to render to. This is :py:obj:`RenderBuffer.BACK` for pbuffers
        surfaces, :py:obj:`RenderBuffer.SINGLE` for pixmap surfaces, and
        whichever was specified on surface creation for window surfaces (the
        default being :py:obj:`RenderBuffer.BACK`).

        The underlying EGL function is ``eglQuerySurface`` with an
        ``attribute`` value of ``EGL_RENDER_BUFFER``.

    .. py:method:: swap_behavior -> SwapBehavior

        :property:

        A property specifying the effect on the colour buffer when the surface
        is posted by a buffer swap.

        The EGL function underlying the getter is ``eglQuerySurface``, while
        the setter calls ``eglSurfaceAttrib``. Each is called with an
        ``attribute`` value of ``EGL_SWAP_BEHAVIOR``.

    .. py:method:: texture_format -> TextureFormat

        :property:

        A read-only property that gets the format for an OpenGL ES texture
        created when binding this (pbuffer) surface to a texture map. The
        value for non-pbuffer surfaces is always
        :py:obj:`TextureFormat.NO_TEXTURE`.

        TODO: Translate NO_TEXTURE to None?

        The underlying EGL function is ``eglQuerySurface`` with an
        ``attribute`` value of ``EGL_TEXTURE_FORMAT``.

    .. py:method:: texture_target -> TextureTarget

        :property:

        A read-only property that gets the target for an OpenGL ES texture
        created when binding this (pbuffer) surface to a texture map. The
        value for non-pbuffer surfaces is always
        :py:obj:`TextureTarget.NO_TEXTURE`.

        TODO: As with texture_format above, do I translate NO_TEXTURE to None?

        The underlying EGL function is ``eglQuerySurface`` with an
        ``attribute`` value of ``EGL_TEXTURE_FORMAT``.

    .. py:method:: vertical_resolution -> Optional[float]

        :property:

        A read-only property that gets the vertical resolution of the display
        on which this (window) surface is visible, in pixels per metre. For a
        non-window surface, the result is None.

        The underlying EGL function is ``eglQuerySurface`` with an
        ``attribute`` value of ``EGL_VERTICAL_RESOLUTION``. The given value
        is scaled by dividing by the value of ``EGL_DISPLAY_SCALING`` (which is
        defined to be 10000).

    .. py:method:: width -> int

        :property:

        A read-only property that gets the width, in pixels, of this surface,
        as most recently registered by the EGL implementation (which may not
        immediately reflect resizing operations from the platform).

        The underlying EGL function is ``eglQuerySurface`` with an
        ``attribute`` value of ``EGL_WIDTH``.

.. py:class:: SurfaceAttrib

    An enumeration of surface attributes.

    - GL_COLORSPACE: the colourspace used by OpenGL and OpenGL ES
    - HEIGHT: the surface's height in pixels
    - LARGEST_PBUFFER: whether or not to get the largest pbuffer available if
      allocation would otherwise fail
    - MIPMAP_TEXTURE: whether or not to allocate storage for OpenGS ES mipmaps
    - RENDER_BUFFER: which buffer client APIs are requested to render to
    - TEXTURE_FORMAT: the format for an OpenGL ES texture created when binding
      a pbuffer to a texture map
    - TEXTURE_TARGET: the target for an OpenGL ES texture created when binding
      a pbuffer to a texture map
    - VG_ALPHA_FORMAT: the alpha format used by OpenVG
    - VG_COLORSPACE: the colourspace used by OpenVG
    - WIDTH: the surface's width in pixels

.. py:class:: GLColorspace

    An enumeration of OpenGL and OpenGL ES colourspaces.

    - GL_COLORSPACE_SRGB (SRGB for short): the sRGB non-linear, perceptually
      uniform colourspace
    - GL_COLORSPACE_LINEAR (LINEAR for short): a linear RGB colourspace

.. py:class:: MultisampleResolve

    An enumeration of filters for resolving the multisample buffer.

    - MULTISAMPLE_RESOLVE_DEFAULT (DEFAULT for short)
    - MULTISAMPLE_RESOLVE_BOX (BOX for short)

.. py:class:: RenderBuffer

    An enumeration of render buffer targets.

    - SINGLE_BUFFER (SINGLE for short)
    - BACK_BUFFER (BACK for short)

.. py:class:: SwapBehavior

    An enumeration of buffer effects when a buffer swap is performed.

    - BUFFER_DESTROYED
    - BUFFER_PRESERVED

.. py:class:: TextureFormat

    An enumeration of texture formats.

    - NO_TEXTURE
    - TEXTURE_RGB (RGB for short)
    - TEXTURE_RGBA (RGBA for short)

.. py:class:: TextureTarget

    An enumeration of texture targets.

    - NO_TEXTURE
    - TEXTURE_2D (2D for short)

.. py:class:: VGAlphaFormat

    An enumeration of OpenVG alpha formats.

    - VG_ALPHA_FORMAT_NONPRE (NONPRE for short): non-premultiplied alpha
    - VG_ALPHA_FORMAT_PRE (PRE for short): premultiplied alpha

.. py:class:: VGColorspace

    An enumeration of OpenVG colourspaces. Note the lower-case "s" in the
    ``sRGB`` colourspace!

    - VG_COLORSPACE_sRGB (sRGB for short): the sRGB non-linear, perceptually
      uniform colourspace
    - VG_COLORSPACE_LINEAR (LINEAR for short): a linear RGB colourspace