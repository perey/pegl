========================
Configuration management
========================

.. py:module:: pegl.config

An EGL configuration is a set of capabilities covering graphics API, color bit
depth, buffer size, and the like. Configurations are obtained from
:py:class:`pegl.display.Display` instances, and once selected, they can be used
to create rendering surfaces and contexts.

The classes and functions listed below are defined in the
:py:mod:`pegl.config` module, but are also imported to the top-level
:py:mod:`pegl` namespace.

The Config class
================

.. py:class:: Config

    A configuration object represents a set of desired graphics capabilities.
    Users should not instantiate this class themselves, but should instead
    get instances from the :py:meth:`~pegl.display.Display.get_configs` or
    :py:meth:`~pegl.display.Display.choose_config` method of a
    :py:class:`~pegl.display.Display` instance.

    Instances of this class are cached; getting an instance with the same
    identifier (the :py:attr:`config_id` property) will result in the same
    object.

    .. todo::
        Caching is not currently working properly. Instances are cached by
        their ``EGLConfig`` handle, not by their ``config_id``. Why EGL makes
        these different things, I don’t know…

    Note that all properties on :py:class:`Config` instances are read-only.

    .. availability:: EGL 1.0

    .. py:method::
        create_context(share_context: Optional[pegl.context.Context]=None, attribs: Optional[dict[pegl.enums.ContextAttrib, Any]]=None) -> pegl.context.Context

        Create a rendering context.

        The underlying EGL function is :eglfunc:`eglCreateContext`.

    .. py:method::
        create_pbuffer_surface(attribs: Optional[dict[pegl.enums.SurfaceAttrib, Any]]=None) -> pegl.surface.Surface

        Create a pbuffer (off-screen) surface.

        The underlying EGL function is :eglfunc:`eglCreatePbufferSurface`.

    .. py:method::
        create_pbuffer_from_client_buffer(buftype: pegl.enums.ClientBufferType, buffer: Any, attribs: Optional[dict[pegl.enums.SurfaceAttrib, Any]]=None) -> pegl.surface.Surface

        Create a pbuffer (off-screen) surface bound to a buffer from a client
        API. The type of buffer is specified by the ``buftype`` argument, and
        an object representing the buffer is passed in the ``buffer`` argument.

        The underlying EGL function is
        :eglfunc:`eglCreatePbufferFromClientBuffer`.

        .. availability:: EGL 1.2

    .. py:method::
        create_pixmap_surface(pixmap: int, attribs: Optional[dict[pegl.enums.SurfaceAttrib, Any]]=None) -> pegl.surface.Surface

        Create a pixmap (off-screen) surface. The ``pixmap`` argument is a
        platform-specific native pixmap object (a ``Pixmap`` on X11, a
        ``HBITMAP`` on Windows, etc.), handled as a ``void *`` in C and as an
        ``int`` in Python.

        The underlying EGL function is :eglfunc:`eglCreatePixmapSurface`.

    .. py:method::
        create_platform_pixmap_surface(native_pixmap: int, attribs: Optional[dict[pegl.enums.SurfaceAttrib, Any]]=None) -> pegl.surface.Surface

        Create a pixmap (off-screen) surface. The ``native_pixmap`` argument is
        a reference to a native pixmap object, handled as a ``void *`` in C and
        as an ``int`` in Python.

        This method is only available in EGL 1.5, but is the preferred
        way to create pixmap surfaces when that version is supported. The
        interpretation of ``native_pixmap`` must be defined by an extension
        that also defines the platform used to create the
        :py:class:`~pegl.display.Display` instance that this configuration
        comes from.

        The underlying EGL function is
        :eglfunc:`eglCreatePlatformPixmapSurface`.

        .. availability:: EGL 1.5

    .. py:method::
        create_platform_window_surface(native_window: int, attribs: Optional[dict[pegl.enums.SurfaceAttrib, Any]]=None) -> pegl.surface.Surface

        Create a window (on-screen) surface. The ``native_window`` argument is
        a reference to a native window object, handled as a ``void *`` in C and
        as an ``int`` in Python.

        This method is only available in EGL 1.5, but is the preferred
        way to create window surfaces when that version is supported. The
        interpretation of ``native_window`` must be defined by an extension
        that also defines the platform used to create the
        :py:class:`~pegl.display.Display` instance that this configuration
        comes from.

        The underlying EGL function is
        :eglfunc:`eglCreatePlatformWindowSurface`.

        .. availability:: EGL 1.5

    .. py:method::
        create_window_surface(win: int, attribs: Optional[dict[pegl.enums.SurfaceAttrib, Any]]=None) -> pegl.surface.Surface

        Create a window (on-screen) surface. The ``win`` argument is a
        platform-specific native window object (an ``ANativeWindow`` on
        Android, a ``HWND`` on Windows, etc.), handled as a ``void *`` in C and
        as an ``int`` in Python.

        The underlying EGL function is :eglfunc:`eglCreateWindowSurface`.

    .. py:method:: get_config_attrib(attribute: pegl.enums.ConfigAttrib) -> int

        Get the value of one of this configuration’s attributes. Users will not
        generally need this function, as the available attributes can be
        queried using specific properties instead.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib`.


    .. py:method:: alpha_mask_size() -> int
        :property:

        The number of bits in the alpha mask buffer.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an ``attribute`` of ``EGL_ALPHA_MASK_SIZE``.

        .. availability:: EGL 1.2

    .. py:method:: alpha_size() -> int
        :property:

        The number of bits in the color buffer allocated to alpha.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an ``attribute`` of ``EGL_ALPHA_SIZE``.

    .. py:method:: bind_to_texture_rgb() -> bool
        :property:

        Whether or not RGB textures can be bound.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_BIND_TO_TEXTURE_RGB``.

        .. availability:: EGL 1.1

    .. py:method:: bind_to_texture_rgba() -> bool
        :property:

        Whether or not RGBA textures can be bound.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_BIND_TO_TEXTURE_RGBA``.

        .. availability:: EGL 1.1

    .. py:method:: blue_size() -> int
        :property:

        The number of bits in the color buffer allocated to blue.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_BLUE_SIZE``.

    .. py:method:: buffer_size() -> int
        :property:

        The total number of color component bits (i.e. not counting any padding
        bits) in the color buffer.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_BUFFER_SIZE``.

    .. py:method:: color_buffer_type() -> pegl.enums.ColorBufferType
        :property:

        The type of color buffer.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_COLOR_BUFFER_TYPE``.

        .. availability::
            EGL 1.2. Prior to this, all color buffers are RGB buffers.

    .. py:method:: config_caveat() -> Optional[pegl.enums.ConfigCaveat]
        :property:

        A caveat that applies when using this configuration. Note that if the
        value would be :py:attr:`pegl.enums.ConfigCaveat.NONE`, a literal
        ``None`` is returned instead.
        
        As of EGL 1.3, the :py:attr:`~pegl.enums.ConfigCaveat.NON_CONFORMANT`
        caveat is obsolete—it applies only to OpenGL ES, whereas the
        :py:attr:`conformant` property gives information on all client APIs.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_CONFIG_CAVEAT``.

    .. py:method:: config_id() -> int
        :property:

        The configuration’s unique identifier.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_CONFIG_ID``.

    .. py:method:: conformant() -> pegl.enums.ClientAPIFlag
        :property:

        A bitmask of client APIs for which conformance requirements will be
        met.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_CONFORMANT``.

        .. availability:: EGL 1.3

    .. py:method:: depth_size() -> int
        :property:

        The number of bits in the depth buffer.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_DEPTH_SIZE``.

    .. py:method:: green_size() -> int
        :property:

        The number of bits in the color buffer allocated to green.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_GREEN_SIZE``.

    .. py:method:: level() -> int
        :property:

        The overlay or underlay level of the frame buffer.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_LEVEL``.

    .. py:method:: luminance_size() -> int
        :property:

        The number of bits in the color buffer allocated to luminance.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_LUMINANCE_SIZE``.

        .. availability:: EGL 1.2

    .. py:method:: max_pbuffer_height() -> int
        :property:

        The maximum pixel width of a pbuffer surface.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_MAX_PBUFFER_HEIGHT``.

    .. py:method:: max_pbuffer_pixels() -> int
        :property:

        The maximum number of pixels in a pbuffer surface.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_MAX_PBUFFER_PIXELS``.

    .. py:method:: max_pbuffer_width() -> int
        :property:

        The maximum pixel height of a pbuffer surface.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_MAX_PBUFFER_WIDTH``.

    .. py:method:: max_swap_interval() -> int
        :property:

        The maximum number of video frames between buffer swaps.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_MAX_SWAP_INTERVAL``.

        .. availability:: EGL 1.1

    .. py:method:: min_swap_interval() -> int
        :property:

        The minimum number of video frames between buffer swaps.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_MIN_SWAP_INTERVAL``.

        .. availability:: EGL 1.1

    .. py:method:: native_renderable() -> bool
        :property:

        Whether or not native rendering APIs can render to a surface.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_NATIVE_RENDERABLE``.

    .. py:method:: native_visual_id() -> int
        :property:

        A platform-specific identifier for the native visual.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_NATIVE_VISUAL_ID``.

    .. py:method:: native_visual_type() -> Any
        :property:

        A platform-defined type for the native visual.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_NATIVE_VISUAL_TYPE``.

    .. py:method:: red_size() -> int
        :property:

        The number of bits in the color buffer allocated to red.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_RED_SIZE``.

    .. py:method:: renderable_type() -> ClientAPIFlag
        :property:

        A bitmask of supported client APIs.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_RENDERABLE_TYPE``.

        .. availability:: EGL 1.2. Prior to this, only OpenGL ES is supported.

    .. py:method:: samples() -> int
        :property:

        The number of samples per pixel.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_SAMPLES``.

    .. py:method:: sample_buffers() -> int
        :property:

        The number of multisample buffers, which is either zero or one.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_SAMPLE_BUFFERS``.

    .. py:method:: stencil_size() -> int
        :property:

        The number of bits in the stencil buffer.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_STENCIL_SIZE``.

    .. py:method:: surface_type() -> pegl.enums.SurfaceTypeFlag
        :property:

        A bitmask of supported surface types.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_SURFACE_TYPE``.

    .. py:method:: transparent_blue_value() -> int
        :property:

        The blue value of the color defined as transparent.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_TRANSPARENT_BLUE_VALUE``.

    .. py:method:: transparent_green_value() -> int
        :property:

        The green value of the color defined as transparent.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_TRANSPARENT_GREEN_VALUE``.

    .. py:method:: transparent_red_value() -> int
        :property:

        The red value of the color defined as transparent.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_TRANSPARENT_RED_VALUE``.

    .. py:method:: transparent_type() -> Optional[pegl.enums.TransparentType]
        :property:

        The type of transparency that is supported. Note that if the value
        would be :py:attr:`pegl.enums.TransparentType.NONE`, a literal ``None``
        is returned instead.

        The underlying EGL function is :eglfunc:`eglGetConfigAttrib` with an
        ``attribute`` of ``EGL_TRANSPARENT_TYPE``.
