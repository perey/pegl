========================
Configuration Management
========================

.. py:module:: pegl.config

This module provides the :py:class:`Config` class. Instances of this class,
which are obtained from :py:class:`Display` instances, represent a
set of capabilities covering graphics API, colour bit depth, buffer size, and
the like. Once selected, a configuration object is used to create rendering
surfaces and contexts.

Configurations
==============

.. py:class:: Config

    A configuration object represents a set of desired graphics capabilities.
    Users should not instantiate this class themselves, but should instead
    get instances from the :py:meth:`Display.get_configs` or
    :py:meth:`Display.choose_config` method of a :py:class:`Display` instance.

    Instances of this class are cached; getting an instance with the same identifier (the :py:method:`config_id` property) will result in the same
    object.

    .. py:method:: create_context(
                       share_context: Optional[Context]=None,
                       attribs: Optional[Dict[ContextAttrib, Any]]=None)
                       -> Context

        Create a rendering context.

        The underlying EGL function is ``eglCreateContext``.

    .. py:method:: create_pbuffer_surface(
                       attribs: Optional[Dict[SurfaceAttrib, Any]]=None)
                       -> Surface

        Create a pbuffer (off-screen) surface.

        The underlying EGL function is ``eglCreatePbufferSurface``.

    .. py:method:: create_pbuffer_surface_from_client_buffer(
                       buftype: ClientBufferType, buffer: Any,
                       attribs: Optional[Dict[SurfaceAttrib, Any]]=None)
                       -> Surface

        Create a pbuffer (off-screen) surface bound to a buffer from a client
        API. The type of buffer is specified by the ``buftype`` argument, and
        an object representing the buffer is passed in the ``buffer`` argument.

        TODO: Only VGImage is supported. Should I just pass a povg.Image object
        and detect the type from that? Or would that create an unworkable
        dependency cycle between pegl and povg? Not to mention an extensibility
        problem...

        The underlying EGL function is
        ``eglCreatePbufferSurfaceFromClientBuffer``.

    .. py:method:: create_pixmap_surface(
                       pixmap: int,
                       attribs: Optional[Dict[SurfaceAttrib, Any]]=None)
                       -> Surface

        Create a pixmap (off-screen) surface. The ``pixmap`` argument is a
        platform-specific native pixmap object (a ``Pixmap`` on X11, a
        ``HBITMAP`` on Windows, etc.), handled as a ``void *`` in C and as an
        ``int`` in Python.

        The underlying EGL function is ``eglCreatePlatformPixmapSurface``.

    .. py:method:: create_platform_pixmap_surface(
                       native_pixmap: int,
                       attribs: Optional[Dict[SurfaceAttrib, Any]]=None)
                       -> Surface

        Create a pixmap (off-screen) surface. The ``native_pixmap`` argument is
        a reference to a native pixmap object, handled as a ``void *`` in C and
        as an ``int`` in Python.

        This method is only available in EGL 1.5, but is the preferred
        way to create pixmap surfaces when that version is supported. The
        interpretation of ``native_pixmap`` must be defined by an extension
        that also defines the platform used to create the :py:class:`Display`
        object that this configuration comes from.

        The underlying EGL function is ``eglCreatePlatformPixmapSurface``.

    .. py:method:: create_platform_window_surface(
                       native_window: int,
                       attribs: Optional[Dict[SurfaceAttrib, Any]]=None)
                       -> Surface

        Create a window (on-screen) surface. The ``native_window`` argument is
        a reference to a native window object, handled as a ``void *`` in C and
        as an ``int`` in Python.

        This method is only available in EGL 1.5, but is the preferred
        way to create window surfaces when that version is supported. The
        interpretation of ``native_window`` must be defined by an extension
        that also defines the platform used to create the :py:class:`Display`
        object that this configuration comes from.

        The underlying EGL function is ``eglCreatePlatformWindowSurface``.

    .. py:method:: create_window_surface(win: int,
                                         attribs: Optional[Dict[SurfaceAttrib,
                                                           Any]]=None)
                       -> Surface

        Create a window (on-screen) surface. The ``win`` argument is a
        platform-specific native window object (an ``ANativeWindow`` on
        Android, a ``HWND`` on Windows, etc.), handled as a ``void *`` in C and
        as an ``int`` in Python.

        The underlying EGL function is ``eglCreateWindowSurface``.

    .. py:method:: get_config_attrib(attribute: ConfigAttrib) -> int

        Get the value of one of this configuration's attribute. Users will not
        generally need this function, as the available attributes can be
        queried using specific properties instead.

        The underlying EGL function is ``eglGetConfigAttrib``.

    .. py:method:: alpha_mask_size -> int

        :property:

        A read-only property giving the number of bits in the alpha mask
        buffer.

        The underlying EGL function is ``eglGetConfigAttrib`` with an ``attribute`` of ``EGL_ALPHA_MASK_SIZE``.

    .. py:method:: alpha_size -> int

        :property:

        A read-only property giving the number of bits in the colour buffer
        allocated to alpha.

        The underlying EGL function is ``eglGetConfigAttrib`` with an ``attribute`` of ``EGL_ALPHA_SIZE``.

    .. py:method:: bind_to_texture_rgb -> bool

        :property:

        A read-only property giving whether or not RGB textures can be bound.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_BIND_TO_TEXTURE_RGB``.

    .. py:method:: bind_to_texture_rgba -> bool

        :property:

        A read-only property giving whether or not RGBA textures can be bound.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_BIND_TO_TEXTURE_RGBA``.

    .. py:method:: blue_size -> int

        :property:

        A read-only property giving the number of bits in the colour buffer
        allocated to blue.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_BLUE_SIZE``.

    .. py:method:: buffer_size -> int

        :property:

        A read-only property giving the total number of colour component bits
        in the colour buffer (i.e. not counting any padding bits).

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_BUFFER_SIZE``.

    .. py:method:: color_buffer_type -> ColorBufferType

        :property:

        A read-only property giving the type of colour buffer.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_COLOR_BUFFER_TYPE``.

    .. py:method:: config_caveat -> Optional[ConfigCaveat]

        :property:

        A read-only property giving any caveats that apply. Note that
        if the value would be :py:attr:`ConfigCaveat.NONE`, a literal None
        is returned instead.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_CONFIG_CAVEAT``.

    .. py:method:: config_id -> int

        :property:

        A read-only property giving the configuration's unique identifier.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_CONFIG_ID``.

    .. py:method:: conformant -> ClientAPIFlag

        :property:

        A read-only property giving the client APIs for which contexts created
        with this configuration will meet conformance requirements.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_CONFORMANT``.

    .. py:method:: depth_size -> int

        :property:

        A read-only property giving the number of bits in the depth buffer.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_DEPTH_SIZE``.

    .. py:method:: green_size -> int

        :property:

        A read-only property giving the number of bits in the colour buffer
        allocated to green.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_GREEN_SIZE``.

    .. py:method:: level -> int

        :property:

        A read-only property giving the overlay or underlay level of the frame
        buffer.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_LEVEL``.

    .. py:method:: luminance_size -> int

        :property:

        A read-only property giving the number of bits in the colour buffer
        allocated to luminance.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_LUMINANCE_SIZE``.

    .. py:method:: max_pbuffer_height -> int

        :property:

        A read-only property giving the maximum pixel width of the pbuffer.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_MAX_PBUFFER_HEIGHT``.

    .. py:method:: max_pbuffer_pixels -> int

        :property:

        A read-only property giving the maximum number of pixels in the
        pbuffer.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_MAX_PBUFFER_PIXELS``.

    .. py:method:: max_pbuffer_width -> int

        :property:

        A read-only property giving the maximum pixel height of the pbuffer.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_MAX_PBUFFER_WIDTH``.

    .. py:method:: max_swap_interval -> int

        :property:

        A read-only property giving the maximum number of video frames between
        buffer swaps.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_MAX_SWAP_INTERVAL``.

    .. py:method:: min_swap_interval -> int

        :property:

        A read-only property giving the minimum number of video frames between
        buffer swaps.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_MIN_SWAP_INTERVAL``.

    .. py:method:: native_renderable -> bool

        :property:

        A read-only property giving whether or not native rendering APIs can render to a surface.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_NATIVE_RENDERABLE``.

    .. py:method:: native_visual_id -> int

        :property:

        A read-only property giving a platform-specific identifier for the native visual.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_NATIVE_VISUAL_ID``.

    .. py:method:: native_visual_type -> int

        :property:

        A read-only property giving a platform-defined type for the native visual.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_NATIVE_VISUAL_TYPE``.

    .. py:method:: red_size -> int

        :property:

        A read-only property giving the number of bits in the colour buffer
        allocated to red.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_RED_SIZE``.

    .. py:method:: renderable_type -> ClientAPIFlag

        :property:

        A read-only property giving which client APIs are supported.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_RENDERABLE_TYPE``.

    .. py:method:: samples -> int

        :property:

        A read-only property giving the number of samples per pixel.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_SAMPLES``.

    .. py:method:: sample_buffers -> int

        :property:

        A read-only property giving the number of multisample buffers, which
        is either zero or one.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_SAMPLE_BUFFERS``.

    .. py:method:: stencil_size -> int

        :property:

        A read-only property giving the number of bits in the stencil buffer.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_STENCIL_SIZE``.

    .. py:method:: surface_type -> SurfaceTypeFlag

        :property:

        A read-only property giving which surface types are supported.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_SURFACE_TYPE``.

    .. py:method:: transparent_blue_value -> int

        :property:

        A read-only property giving the blue value of the colour defined as transparent.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_TRANSPARENT_BLUE_VALUE``.

    .. py:method:: transparent_green_value -> int

        :property:

        A read-only property giving the green value of the colour defined as transparent.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_TRANSPARENT_GREEN_VALUE``.

    .. py:method:: transparent_red_value -> int

        :property:

        A read-only property giving the red value of the colour defined as transparent.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_TRANSPARENT_RED_VALUE``.

    .. py:method:: transparent_type -> TransparentType

        :property:

        A read-only property giving which type of transparency is supported.
        Note that if the value would be :py:attr:`TransparentType.NONE`, a
        literal None is returned instead.

        The underlying EGL function is ``eglGetConfigAttrib`` with an
        ``attribute`` of ``EGL_TRANSPARENT_TYPE``.

.. py:class:: ConfigAttrib

    An enumeration of configuration attributes. These are used when requesting
    a configuration object that meets an application's requirements.

    - ALPHA_MASK_SIZE: the number of bits in the alpha mask buffer
    - ALPHA_SIZE: the number of bits in the colour buffer allocated to alpha
    - BIND_TO_TEXTURE_RGB: whether or not RGB textures can be bound
    - BIND_TO_TEXTURE_RGBA: whether or not RGBA textures can be bound
    - BLUE_SIZE: the number of bits in the colour buffer allocated to blue
    - BUFFER_SIZE: the total number of colour component bits in the colour
      buffer (i.e. not counting any padding bits)
    - CONFIG_CAVEAT: any caveats that apply
    - COLOR_BUFFER_TYPE: the type of colour buffer
    - CONFIG_ID: the configuration's unique identifier
    - CONFORMANT: the conformance requirements that must be met
    - DEPTH_SIZE: the number of bits in the depth buffer
    - GREEN_SIZE: the number of bits in the colour buffer allocated to green
    - LEVEL: the overlay or underlay level of the frame buffer
    - LUMINANCE_SIZE: the number of bits in the colour buffer allocated to
      luminance
    - MATCH_NATIVE_PIXMAP: a platform-specific identifier for a pixmap that
      this configuration must support rendering to
    - MAX_PBUFFER_HEIGHT: the maximum pixel width of the pbuffer
    - MAX_PBUFFER_PIXELS: the maximum number of pixels in the pbuffer
    - MAX_PBUFFER_WIDTH: the maximum pixel height of the pbuffer
    - MAX_SWAP_INTERVAL: the maximum swap interval, in video frame periods
    - MIN_SWAP_INTERVAL: the maximum swap interval, in video frame periods
    - NATIVE_RENDERABLE: whether or not native rendering APIs can render to a
      surface
    - NATIVE_VISUAL_ID: a platform-specific identifier for the native visual
    - NATIVE_VISUAL_TYPE: a platform-defined type for the native visual
    - RED_SIZE: the number of bits in the colour buffer allocated to red
    - RENDERABLE_TYPE: which client APIs are supported
    - SAMPLES: the number of samples per pixel
    - SAMPLE_BUFFERS: the number of multisample buffers (either 0 or 1)
    - STENCIL_SIZE: the number of bits in the stencil buffer
    - SURFACE_TYPE: which surface types are supported
    - TRANSPARENT_BLUE_VALUE: the blue value of the colour defined as
      transparent
    - TRANSPARENT_GREEN_VALUE: the green value of the colour defined as
      transparent
    - TRANSPARENT_RED_VALUE: the red value of the colour defined as transparent
    - TRANSPARENT_TYPE: which type of transparency is supported

.. py:class:: ColorBufferType

    An enumeration giving the following types of colour buffer.

    - RGB_BUFFER (RGB for short)
    - LUMINANCE_BUFFER (LUMINANCE for short)

.. py:class:: SurfaceTypeFlag

    An enumeration of flags describing surfaces supported by a configuration.
    Despite the name, this includes both surface types (the first three flags
    below) and available attributes.

    - PBUFFER_BIT (PBUFFER for short): pbuffers are supported
    - PIXMAP_BIT (PIXMAP for short): pixmaps are supported
    - WINDOW_BIT (WINDOW for short): windows are supported
    - MULTISAMPLE_RESOLVE_BOX_BIT (MULTISAMPLE_RESOLVE_BOX for short):
      box-filtered multisample resolve is supported
    - SWAP_BEHAVIOUR_PRESERVED_BIT (SWAP_BEHAVIOUR_PRESERVED for short):
      setting swap behaviour to preserve colour buffers is supported
    - VG_ALPHA_FORMAT_PRE_BIT (VG_ALPHA_FORMAT_PRE for short): OpenVG rendering
      with premultiplied alpha is supported
    - VG_COLORSPACE_LINEAR_BIT (VG_COLORSPACE_LINEAR for short): OpenVG
      rendering in linear colourspace is supported

.. py:class:: ClientAPIFlag

    An enumeration of flags identifying the client APIs supported by a
    configuration.

    - OPENGL_BIT (OPENGL for short): OpenGL (any version) is supported
    - OPENGL_ES_BIT (OPENGL_ES for short): OpenGL ES 1.x is supported
    - OPENGL_ES2_BIT (OPENGL_ES2 for short): OpenGL ES 2.x is supported
    - OPENGL_ES3_BIT (OPENGL_ES3 for short): OpenGL ES 3.x is supported
    - OPENVG_BIT (OPENVG for short): OpenGL ES 1.x is supported

.. py:class:: ConfigCaveat

    An enumeration of caveats that may apply to a configuration.

    - NONE
    - SLOW_CONFIG
    - NON_CONFORMANT_CONFIG (obsolete)

.. py:class:: TransparentType

    An enumeration of transparency types that may be supported.

    - NONE
    - TRANSPARENT_RGB (RGB for short)

.. py:class:: ClientBufferType

    An enumeration of client API buffer types.

    - OPENVG_IMAGE: an OpenVG ``VGImage`` buffer