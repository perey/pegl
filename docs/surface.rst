==================
Rendering surfaces
==================

.. py:module:: pegl.surface

A surface is the target for rendering operations (and, in some cases, for
reading information on what has been rendered).

There are three types of surfaces in EGL. Window surfaces are for on-screen
display. Pbuffer surfaces are off-screen surfaces stored in graphics memory.
Pixmap surfaces are off-screen surfaces that correspond to a native platform
pixmap (image).

The :py:class:`Surface` class is defined in the :py:mod:`pegl.surface` module,
but it is also imported to the top-level :py:mod:`pegl` namespace.

The Surface class
=================

.. py:class:: Surface

    A surface represents a target to which graphics can be rendered. Users
    should not instantiate this class themselves, but should instead get an
    instance from the relevant :py:class:`~pegl.config.Config` method (one of
    :py:meth:`~pegl.config.Config.create_pbuffer_surface`,
    :py:meth:`~pegl.config.Config.create_pbuffer_surface_from_client_buffer`,
    :py:meth:`~pegl.config.Config.create_pixmap_surface`,
    :py:meth:`~pegl.config.Config.create_platform_pixmap_surface`,
    :py:meth:`~pegl.config.Config.create_platform_window_surface`, or
    :py:meth:`~pegl.config.Config.create_window_surface`).

    Instances of this class are cached until their destructor is called, so
    that they can be retrieved by the
    :py:meth:`pegl.context.Context.get_current_surface` class method and its
    property shortcuts.

    The EGL function underlying the destructor is :eglfunc:`eglDestroySurface`.

    .. availability:: EGL 1.0

    .. py:method::
        bind_tex_image(buffer: pegl.enums.RenderBuffer=pegl.enums.RenderBuffer.BACK) -> None

        Bind the given buffer of this (pbuffer) surface as a texture. Note that
        only the :py:obj:`~pegl.enums.RenderBuffer.BACK` buffer is allowed,
        even for a single-buffered surface, as it indicates the buffer into
        which rendering is taking place. As such, the ``buffer`` argument may be omitted.

        The underlying EGL function is :eglfunc:`eglBindTexImage`.

        .. availability:: EGL 1.1

    .. py:method:: copy_buffers(target: int) -> None

        Copy the color buffer of this surface to a native pixmap. The
        ``target`` argument is a platform-specific native pixmap object (a
        ``Pixmap`` on X11, a ``HBITMAP`` on Windows, etc.), handled as a
        ``void *`` in C and as an ``int`` in Python.

        The underlying EGL function is :eglfunc:`eglCopyBuffers`.

    .. py:method::
        release_tex_image(buffer: pegl.enums.RenderBuffer=pegl.enums.RenderBuffer.BACK) -> None

        Release the given buffer of this (pbuffer) surface from its binding as
        a texture. Note that only the :py:obj:`~pegl.enums.RenderBuffer.BACK`
        buffer is allowed, even for a single-buffered surface, as it indicates
        the buffer into which rendering is taking place. As such, the ``buffer`` argument may be omitted.

        While this method undoes the effect of :py:meth:`bind_tex_image`, it is
        not an error to call it when the buffer is not actually bound.

        The underlying EGL function is :eglfunc:`eglReleaseTexImage`.

        .. availability:: EGL 1.1

    .. py:method:: swap_buffers() -> None

        Post the back color buffer of this (window) surface to the window.
        This method is available but has no effect on pbuffer, pixmap, and
        single-buffered window surfaces.

        The underlying EGL function is :eglfunc:`eglSwapBuffers`.

    .. py:method:: config() -> pegl.config.Config
        :property:

        The config used to create this surface. Read-only.

        The underlying EGL function is :eglfunc:`eglQuerySurface` with an
        ``attribute`` value of ``EGL_CONFIG_ID``.

    .. py:method:: config_id() -> int
        :property:

        The unique identifier of the config used to create this surface.
        Read-only.

        For most users, the :py:attr:`config` property will be more useful.

        The underlying EGL function is :eglfunc:`eglQuerySurface` with an
        ``attribute`` value of ``EGL_CONFIG_ID``.

    .. py:method:: height() -> int
        :property:

        The pixel height of this surface, as most recently registered by the
        EGL implementation (which may not immediately reflect resizing
        operations from the platform). Read-only.

        The underlying EGL function is :eglfunc:`eglQuerySurface` with an
        ``attribute`` value of ``EGL_HEIGHT``.

    .. py:method:: horizontal_resolution() -> Optional[float]
        :property:

        The horizontal resolution of the display on which this (window) surface
        is visible, in pixels per metre. Read-only.

        For a non-window surface, or where the value is unknown, the result is
        ``None``.

        The underlying EGL function is :eglfunc:`eglQuerySurface` with an
        ``attribute`` value of ``EGL_HORIZONTAL_RESOLUTION``. EGL provides an
        integer value, which is scaled down to a ``float`` by dividing by the 
        value of ``EGL_DISPLAY_SCALING`` (which is defined to be 10 000).

        .. availability:: EGL 1.2

    .. py:method:: largest_pbuffer() -> bool
        :property:

        When this (pbuffer) surface was created, was the EGL implementation
        allowed to return the largest available pbuffer if the requested pbuffer could not be created? Read-only.

        This is always ``False`` for non-pbuffer surfaces.

        The underlying EGL function is :eglfunc:`eglQuerySurface` with an
        ``attribute`` value of ``EGL_LARGEST_PBUFFER``.

    .. py:method:: mipmap_level() -> int
        :property:

        Which level of the OpenGL ES mipmap texture should be rendered.

        The EGL function underlying the getter is :eglfunc:`eglQuerySurface`,
        while the setter calls :eglfunc:`eglSurfaceAttrib`. Each is called with
        an ``attribute`` value of ``EGL_MIPMAP_LEVEL``.

        .. availability:: EGL 1.1

    .. py:method:: mipmap_texture() -> bool
        :property:

        Whether or not storage should be allocated for OpenGL ES mipmaps.
        Read-only.

        The underlying EGL function is :eglfunc:`eglQuerySurface` with an
        ``attribute`` value of ``EGL_MIPMAP_TEXTURE``.

        .. availability:: EGL 1.1

    .. py:method:: multisample_resolve() -> pegl.enums.MultisampleResolve
        :property:

        The filter method used for resolving the multisample buffer.

        The EGL function underlying the getter is :eglfunc:`eglQuerySurface`,
        while the setter calls :eglfunc:`eglSurfaceAttrib`. Each is called with
        an ``attribute`` value of ``EGL_MULTISAMPLE_RESOLVE``.

        .. availability:: EGL 1.4

    .. py:method:: pixel_aspect_ratio() -> Optional[float]
        :property:

        The pixel aspect ratio (width divided by height) of the display on
        which this (window) surface is visible. Read-only.

        For a non-window surface, or where the value is unknown, the result is
        ``None``.

        The underlying EGL function is :eglfunc:`eglQuerySurface` with an
        ``attribute`` value of ``EGL_PIXEL_ASPECT_RATIO``. EGL provides an
        integer value, which is scaled down to a ``float`` by dividing by the 
        value of ``EGL_DISPLAY_SCALING`` (which is defined to be 10 000).

        .. availability:: EGL 1.2

    .. py:method:: render_buffer() -> pegl.enums.RenderBuffer
        :property:

        Which buffer are client APIs requested to render to? Read-only.

        This is always :py:obj:`~pegl.enums.RenderBuffer.BACK` for pbuffer
        surfaces, and :py:obj:`~pegl.enums.RenderBuffer.SINGLE` for pixmap surfaces.

        The underlying EGL function is :eglfunc:`eglQuerySurface` with an
        ``attribute`` value of ``EGL_RENDER_BUFFER``.

        .. availability:: EGL 1.1

    .. py:method:: swap_behavior() -> pegl.enums.SwapBehavior
        :property:

        The effect on the color buffer when the surface is posted by a buffer
        swap.

        The EGL function underlying the getter is :eglfunc:`eglQuerySurface`,
        while the setter calls :eglfunc:`eglSurfaceAttrib`. Each is called with
        an ``attribute`` value of ``EGL_SWAP_BEHAVIOR``.

        .. availability:: EGL 1.2

    .. py:method:: texture_format() -> Optional[pegl.enums.TextureFormat]
        :property:

        The format for an OpenGL ES texture created when binding this (pbuffer)
        surface to a texture map. Read-only.

        The value for non-pbuffer surfaces is always ``None`` (representing
        :py:obj:`~pegl.enums.TextureFormat.NO_TEXTURE`).

        The underlying EGL function is :eglfunc:`eglQuerySurface` with an
        ``attribute`` value of ``EGL_TEXTURE_FORMAT``.

        .. availability:: EGL 1.1

    .. py:method:: texture_target() -> Optional[pegl.enums.TextureTarget]
        :property:

        The target for an OpenGL ES texture created when binding this (pbuffer)
        surface to a texture map.

        The value for non-pbuffer surfaces is always ``None`` (representing
        :py:obj:`~pegl.enums.TextureTarget.NO_TEXTURE`)

        The underlying EGL function is :eglfunc:`eglQuerySurface` with an
        ``attribute`` value of ``EGL_TEXTURE_FORMAT``.

        .. availability:: EGL 1.1

    .. py:method:: vertical_resolution() -> Optional[float]
        :property:

        The vertical resolution of the display on which this (window) surface
        is visible, in pixels per metre. Read-only.

        For a non-window surface, or where the value is unknown, the result is
        ``None``.

        The underlying EGL function is :eglfunc:`eglQuerySurface` with an
        ``attribute`` value of ``EGL_VERTICAL_RESOLUTION``. EGL provides an
        integer value, which is scaled down to a ``float`` by dividing by the 
        value of ``EGL_DISPLAY_SCALING`` (which is defined to be 10 000).

        .. availability:: EGL 1.2

    .. py:method:: width() -> int
        :property:

        The width, in pixels, of this surface, as most recently registered by
        the EGL implementation (which may not immediately reflect resizing
        operations from the platform). Read-only.

        The underlying EGL function is :eglfunc:`eglQuerySurface` with an
        ``attribute`` value of ``EGL_WIDTH``.
