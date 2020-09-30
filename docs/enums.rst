============
Enumerations
============

.. py:module:: pegl.enums

Many of the constants defined in EGL are organized into the following
enumerations. These are defined in the :py:mod:`pegl.enums` module, but are
also imported to the top-level :py:mod:`pegl` namespace.

Each constant is available under its original name minus the ``EGL_`` prefix.
Many are also given shorter names, where the longer form is redundant with the
enumeration name (e.g. :py:attr:`ContextAttrib.CONTEXT_CLIENT_TYPE` has the
shorter name :py:attr:`ContextAttrib.CLIENT_TYPE`). The suffixes ``_BIT`` and
``_MASK`` are implied by an enumeration being a flag (bitmask) type, and by an
attribute taking values from a flag (bitmask) enumeration, respectively, so
these are also left out of short names.

.. todo::
    For enumerations with ``NONE`` as a value, and possibly others
    (:py:class:`TextureFormat.NO_TEXTURE` and
    :py:class:`TextureTarget.NO_TEXTURE`) where the matching query can return
    ``None``, attribute lists (or other ways of setting values, if there are
    any?) should accept ``None`` and adapt it accordingly.

.. py:class:: ClientAPI

    Client APIs supported by EGL.

    .. availability:: EGL 1.2

    .. py:attribute:: OPENGL

        The OpenGL_ API. The longer form :py:attr:`OPENGL_API` is provided as
        an alias.

        .. availability:: EGL 1.4

    .. py:attribute:: OPENGL_ES

        The `OpenGL ES`_ API. The longer form :py:attr:`OPENGL_ES_API` is
        provided as an alias.

    .. py:attribute:: OPENVG

        The OpenVG_ API. The longer form :py:attr:`OPENVG_API` is provided as
        an alias.

.. _OpenGL: https://www.khronos.org/opengl/
.. _`OpenGL ES`: https://www.khronos.org/opengles/
.. _OpenVG: https://www.khronos.org/openvg/


.. py:class:: ClientAPIFlag

    Flags for client APIs supported, used when requesting a config or when
    querying the attributes of one. Compared with :py:class:`ClientAPI`, these
    are more specific (identifying particular versions) and, as flags, can be
    combined.

    .. availability:: EGL 1.2

    .. py:attribute:: NONE
    
        No particular client API is required to be supported.

    .. py:attribute:: OPENGL

        Any version of OpenGL is supported. The longer form
        :py:attr:`OPENGL_BIT` is provided as an alias.

        .. availability:: EGL 1.4

    .. py:attribute:: OPENGL_ES

        OpenGL ES 1.x is supported. The longer form :py:attr:`OPENGL_ES_BIT`
        is provided as an alias.

    .. py:attribute:: OPENGL_ES2

        OpenGL ES 2.x is supported. The longer form :py:attr:`OPENGL_ES2_BIT`
        is provided as an alias.

        .. availability:: EGL 1.3

    .. py:attribute:: OPENGL_ES3

        OpenGL ES 3.x is supported. The longer form :py:attr:`OPENGL_ES3_BIT`
        is provided as an alias.

        .. availability:: EGL 1.5

    .. py:attribute:: OPENVG

        OpenVG 1.x is supported. The longer form :py:attr:`OPENVG_BIT` is provided as an alias.


.. py:class:: ClientBufferType

    Client API buffer types that can be used to create pbuffer surfaces. Only
    one such type is given in the core specification.

    .. availability:: EGL 1.2

    .. py:attribute:: OPENVG_IMAGE

        An OpenVG ``VGImage`` buffer.


.. py:class:: ColorBufferType

    Types of color buffer that may be supported by a config.

    .. availability:: EGL 1.2

    .. py:attribute:: RGB

        RGB buffers are supported. The longer form :py:attr:`RGB_BUFFER` is
        provided as an alias.

    .. py:attribute:: LUMINANCE

        Luminance buffers are supported. The longer form
        :py:attr:`LUMINANCE_BUFFER` is provided as an alias.


.. py:class:: ConfigAttrib

    Configuration attributes used when requesting a config that meets an
    application’s requirements. The allowed values are described below.

    .. availability:: EGL 1.0

    .. py:attribute:: ALPHA_MASK_SIZE

        The number of bits in the alpha mask buffer (an ``int``).

        .. availability:: EGL 1.2

    .. py:attribute:: ALPHA_SIZE:

        The number of bits in the color buffer allocated to alpha (an ``int``).

    .. py:attribute:: BIND_TO_TEXTURE_RGB

        Whether or not RGB textures can be bound (a ``bool``).

        .. availability:: EGL 1.1

    .. py:attribute:: BIND_TO_TEXTURE_RGBA

        Whether or not RGBA textures can be bound (a ``bool``).

        .. availability:: EGL 1.1

    .. py:attribute:: BLUE_SIZE

        The number of bits in the color buffer allocated to blue (an ``int``).

    .. py:attribute:: BUFFER_SIZE

        The total number of color component bits (i.e. not counting any padding
        bits) in the color buffer (an ``int``).

    .. py:attribute:: CONFIG_CAVEAT

        Any caveats that apply (a value from :py:class:`ConfigCaveat`).

    .. py:attribute:: COLOR_BUFFER_TYPE

        The type of color buffer supported (a value from
        :py:class:`ColorBufferType`).

        .. availability::
            EGL 1.2. Prior to this, only RGB buffers are supported.

    .. py:attribute:: CONFIG_ID

        The requested configuration’s unique identifier (an ``int``). When this
        is specified, all other requested attributes are ignored.

    .. py:attribute:: CONFORMANT

        The conformance requirements that must be met (a combination of values
        from :py:class:`ClientAPIFlag`).

        .. availability:: EGL 1.3

    .. py:attribute:: DEPTH_SIZE

        The number of bits in the depth buffer (an ``int``).

    .. py:attribute:: GREEN_SIZE

        The number of bits in the color buffer allocated to green (an ``int``).

    .. py:attribute:: LEVEL

        The overlay or underlay level of the frame buffer (an ``int``).

    .. py:attribute:: LUMINANCE_SIZE

        The number of bits in the color buffer allocated to luminance (an
        ``int``).

        .. availability:: EGL 1.2

    .. py:attribute:: MATCH_NATIVE_PIXMAP

        A handle for a pixmap to which a configuration must support rendering
        (a platform-specific type, handled as an ``int``).

        .. availability:: EGL 1.3

    .. py:attribute:: MAX_PBUFFER_HEIGHT

        The maximum pixel width of a pbuffer surface (an ``int``).

    .. py:attribute:: MAX_PBUFFER_PIXELS

        The maximum number of pixels in a pbuffer surface (an ``int``).

    .. py:attribute:: MAX_PBUFFER_WIDTH

        The maximum pixel height of a pbuffer surface (an ``int``).

    .. py:attribute:: MAX_SWAP_INTERVAL

        The maximum interval, in video frames, between buffer swaps (an
        ``int``).

        .. availability:: EGL 1.1

    .. py:attribute:: MIN_SWAP_INTERVAL

        The minimum interval, in video frame, between buffer swaps (an
        ``int``).

        .. availability:: EGL 1.1

    .. py:attribute:: NATIVE_RENDERABLE

        Whether or not native rendering APIs can render to a surface (a
        ``bool``).

    .. py:attribute:: NATIVE_VISUAL_ID

        A handle for a native visual (a platform-specific type, handled as an
        ``int``).

    .. py:attribute:: NATIVE_VISUAL_TYPE

        The type of native visual supported (a platform-defined type, handled
        as an ``int``).

    .. py:attribute:: RED_SIZE

        The number of bits in the color buffer allocated to red (an ``int``).

    .. py:attribute:: RENDERABLE_TYPE

        Which client APIs are supported (a combination of values from
        :py:class:`ClientAPIFlag`)

        .. availability:: EGL 1.2. Prior to this, only OpenGL ES is supported.

    .. py:attribute:: SAMPLES

        The number of samples per pixel (an ``int``).

    .. py:attribute:: SAMPLE_BUFFERS

        The number of multisample buffers (an ``int``, either 0 or 1).

    .. py:attribute:: STENCIL_SIZE

        The number of bits in the stencil buffer (an ``int``).

    .. py:attribute:: SURFACE_TYPE

        Which surface types and attributes are supported (a combination of
        values from :py:class:`SurfaceTypeFlag`).

    .. py:attribute:: TRANSPARENT_BLUE_VALUE

        The blue value of the color defined as transparent (an ``int``).

    .. py:attribute:: TRANSPARENT_GREEN_VALUE

        The green value of the color defined as transparent (an ``int``).

    .. py:attribute:: TRANSPARENT_RED_VALUE

        The red value of the color defined as transparent (an ``int``).

    .. py:attribute:: TRANSPARENT_TYPE

        The type of transparency supported (a value from
        :py:class:`TransparentType`).


.. py:class:: ConfigCaveat

    Caveats that may apply to a configuration.

    .. availability:: EGL 1.0

    .. py:attribute:: NONE

        No caveat applies.

    .. py:attribute:: SLOW

        Rendering to a surface with this configuration may be slow, for
        instance because there is no hardware support for the requested
        buffer size. The longer form :py:attr:`SLOW_CONFIG` is provided as an
        alias.

    .. py:attribute:: NON_CONFORMANT

        OpenGL ES conformance requirements will not be met. (This value is
        obsolete in EGL 1.3 and later, since
        :py:attr:`~ConfigAttrib.CONFORMANT` can be used to specify conformance
        for *any* client API.) The longer form :py:attr:`NON_CONFORMANT_CONFIG`
        is provided as an alias.


.. py:class:: ContextAttrib

    Rendering context attributes that may be requested when creating a context.
    The allowed values are noted below.

    Many attributes are relevant only to specific client APIs, which is also
    noted below. A few attributes may be queried from existing contexts, but
    they are accessed through properties, not by using this enumeration.

    .. availability:: EGL 1.2

    .. py:attribute:: CLIENT_TYPE

        The client API that this context will support (a value from
        :py:class:`ClientAPI`). The longer form :py:attr:`CONTEXT_CLIENT_TYPE` is provided as an alias.

    .. py:attribute:: CLIENT_VERSION

        The major version number of the client API to support (an ``int``).
        Only valid for OpenGL and OpenGL ES.

        From EGL 1.5, the name of this attribute is changed to
        :py:attr:`MAJOR_VERSION` (presumably to match
        :py:attr:`MINOR_VERSION`); this name is provided as an alias,
        regardless of EGL version. The longer forms
        :py:attr:`CONTEXT_CLIENT_VERSION` and :py:attr:`CONTEXT_MAJOR_VERSION`
        are also provided as aliases.

        .. availability:: EGL 1.3

    .. py:attribute:: MINOR_VERSION

        The minor version number of the client API requested (an ``int``). Only
        valid for OpenGL and OpenGL ES. The longer form
        :py:attr:`CONTEXT_MINOR_VERSION` is provided as an alias.

        .. availability:: EGL 1.5

    .. py:attribute:: OPENGL_DEBUG

        Whether or not the context must support debugging functionality (a
        ``bool``). Only valid for OpenGL and OpenGL ES with the relevant
        extension or core functionality, though it is ignored, not an error,
        when debug contexts are not supported. The longer form
        :py:attr:`CONTEXT_OPENGL_DEBUG` is provided as an alias.

        .. availability:: EGL 1.5

    .. py:attribute:: OPENGL_FORWARD_COMPATIBLE

        Whether or not the context must be forward-compatible (a ``bool``).
        Only valid for OpenGL 3.0 and later. The longer form
        :py:attr:`CONTEXT_OPENGL_FORWARD_COMPATIBLE` is provided as an alias.

        .. availability:: EGL 1.5

    .. py:attribute:: OPENGL_PROFILE

        The OpenGL profile requested (a combination of values from
        :py:class:`OpenGLProfileFlag`). Only valid for OpenGL 3.2 and later,
        though it is ignored, not an error, on earlier versions of OpenGL.
        The longer form :py:attr:`CONTEXT_OPENGL_PROFILE_MASK` is provided as
        an alias.

        .. availability:: EGL 1.5

    .. py:attribute:: OPENGL_RESET_NOTIFICATION_STRATEGY

        The reset notification strategy to use when the context supports robust
        buffer access (a value from :py:class:`ResetNotificationStrategy`).
        Specifying this when robust access is not demanded (as above) is not an
        error, but may not in itself result in a context supporting robust
        buffer access. Only valid for OpenGL and OpenGL ES with the relevant
        extension or core functionality.  The longer form
        :py:attr:`CONTEXT_OPENGL_RESET_NOTIFICATION_STRATEGY` is provided as an
        alias.

        .. availability:: EGL 1.5

    .. py:attribute:: OPENGL_ROBUST_ACCESS

        Whether or not the context must support robust buffer access (a
        ``bool``). Only valid OpenGL and OpenGL ES with the relevant extension
        or core functionality. The longer form
        :py:attr:`CONTEXT_OPENGL_ROBUST_ACCESS` is provided as an alias.

        .. availability:: EGL 1.5


.. py:class:: DisplayAttrib

    Display attributes that may be specified when calling
    :py:meth:`pegl.display.Display.get_platform_display`. This enumeration is
    left empty by the core EGL specification.

    .. availability:: EGL 1.5


.. py:class:: GLColorspace

    Colorspaces supported by OpenGL and OpenGL ES.

    .. availability:: EGL 1.5

    .. py:attribute:: LINEAR

        A linear RGB colorspace. The longer form
        :py:attr:`GL_COLORSPACE_LINEAR` is provided as an alias.

    .. py:attribute:: SRGB

        The sRGB non-linear, perceptually uniform colorspace. The longer form :py:attr:`GL_COLORSPACE_SRGB` is provided as an alias.

        Note that unlike :py:class:`VGColorspace`, “SRGB” is here written with
        a capital S. To avoid hard-to-detect errors, short and long aliases
        with the lower-case S are also provided.


.. py:class:: ImageAttrib

    Attributes that can be specified when creating an image. No EGL mechanism
    is currently provided for querying these after image creation.

    .. availability:: EGL 1.5

    .. py:attribute:: GL_TEXTURE_LEVEL
    .. py:attribute:: GL_TEXTURE_ZOFFSET
    .. py:attribute:: IMAGE_PRESERVED


.. py:class:: ImageTarget

    The target (type of resource) to be used as the source for creating an
    image. Only OpenGL and OpenGL ES targets are provided in the core
    specification.

    .. availability:: EGL 1.5

    .. py:attribute:: GL_TEXTURE_2D

        The 2D texture.

    .. py:attribute:: GL_TEXTURE_CUBE_MAP_POSITIVE_X

        The positive X face of the cube map texture.

    .. py:attribute:: GL_TEXTURE_CUBE_MAP_NEGATIVE_X

        The negative X face of the cube map texture.

    .. py:attribute:: GL_TEXTURE_CUBE_MAP_POSITIVE_Y

        The positive Y face of the cube map texture.

    .. py:attribute:: GL_TEXTURE_CUBE_MAP_NEGATIVE_Y

        The negative Y face of the cube map texture.

    .. py:attribute:: GL_TEXTURE_CUBE_MAP_POSITIVE_Z

        The positive Z face of the cube map texture.

    .. py:attribute:: GL_TEXTURE_CUBE_MAP_NEGATIVE_Z

        The negative Z face of the cube map texture.

    .. py:attribute:: GL_TEXTURE_3D

        The 3D texture.

    .. py:attribute:: GL_RENDERBUFFER

        The renderbuffer.


.. py:class:: MultisampleResolve

    Filters that may be used for resolving the multisample buffer.

    .. availability:: EGL 1.4

    .. py:attribute:: BOX

        A one-pixel wide, equal-weight box filter. The longer form
        :py:attr:`MULTISAMPLE_RESOLVE_BOX` is provided as an alias.

    .. py:attribute:: DEFAULT

        The implementation’s default filter. The longer form
        :py:attr:`MULTISAMPLE_RESOLVE_DEFAULT` is provided as an alias.


.. py:class:: NativeEngine

    Native rendering engines recognised by the EGL implementation (that is,
    those not classified as client APIs: OpenGL, OpenGL ES, and OpenVG).

    .. availability:: EGL 1.0

    .. py:attribute:: CORE

        The most commonly used engine on the current platform, as defined
        by the EGL implementation. The longer form
        :py:attr:`CORE_NATIVE_ENGINE` is provided as an alias.


.. py:class:: OpenGLProfileFlag

    Flags for OpenGL profiles.

    .. availability:: EGL 1.5

    .. py:attribute:: NONE
    
        No particular OpenGL profile is identified.

    .. py:attribute:: CORE

        The core profile. The longer form
        :py:attr:`CONTEXT_OPENGL_CORE_PROFILE_BIT` is provided as an alias.

    .. py:attribute:: COMPATIBILITY

        The compatibility profile. The longer form :py:attr:`CONTEXT_OPENGL_COMPATIBILITY_PROFILE_BIT` is provided as an
        alias.


.. py:class:: Platform

    Known platforms that may be specified when calling
    :py:meth:`pegl.display.Display.get_platform_display`. This enumeration is
    left empty by the core EGL specification.

    .. availability:: EGL 1.5


.. py:class:: ReadOrDraw

    Which surface, the one bound for reading or for drawing, is requested.

    .. availability:: EGL 1.0

    .. py:attribute:: DRAW

        The surface bound for drawing is requested.

    .. py:attribute:: READ

        The surface bound for reading is requested.


.. py:class:: RenderBuffer

    Buffer targets for rendering.

    .. availability:: EGL 1.1

    .. py:attribute:: BACK

        The surface’s back buffer is targeted. The longer form
        :py:attr:`BACK_BUFFER` is provided as an alias.

    .. py:attribute:: SINGLE

        The surface’s only buffer is targeted. The longer form
        :py:attr:`SINGLE_BUFFER` is provided as an alias.

        .. availability:: EGL 1.2


.. py:class:: ResetNotificationStrategy

    OpenGL and OpenGL ES reset notification strategies.

    .. availability:: EGL 1.5

    .. py:attribute:: LOSE_CONTEXT_ON_RESET

        Context state is lost on reset, and applications may ask for
        notification of reset events.

    .. py:attribute:: NO_RESET_NOTIFICATION

        No notification of reset events is given. Context state should not be
        lost, but this cannot be relied on.


.. py:class:: SurfaceAttrib

    Rendering surface attributes that may be requested when creating a surface.
    The allowed values are described below.

    Once a surface is created, each attribute may be queried using properties
    of the :py:class:`pegl.surface.Surface` instance, not by using this
    enumeration.

    .. availability:: EGL 1.0

    .. py:attribute:: GL_COLORSPACE

        The colorspace used by OpenGL and OpenGL ES (a value from
        :py:class:`GLColorspace`).

        .. availability:: EGL 1.5

    .. py:attribute:: HEIGHT

        The surface’s height in pixels (an ``int``).

    .. py:attribute:: LARGEST_PBUFFER

        Whether or not to get the largest pbuffer available if allocation would
        otherwise fail (a ``bool``).

    .. py:attribute:: MIPMAP_TEXTURE

        Whether or not to allocate storage for OpenGS ES mipmaps (a ``bool``).

        .. availability:: EGL 1.1

    .. py:attribute:: RENDER_BUFFER

        Which buffer client APIs are requested to render to (a value from
        :py:class:`RenderBuffer`).

        .. availability:: EGL 1.2

    .. py:attribute:: TEXTURE_FORMAT

        The format for an OpenGL ES texture created when binding a pbuffer
        surface to a texture map (a value from :py:class:`TextureFormat`).

        .. availability:: EGL 1.1

    .. py:attribute:: TEXTURE_TARGET

        The target for an OpenGL ES texture created when binding a pbuffer
        surface to a texture map (a value from :py:class:`TextureTarget`).

        .. availability:: EGL 1.1

    .. py:attribute:: VG_ALPHA_FORMAT

        The alpha format used by OpenVG (a value from
        :py:class:`VGAlphaFormat`).

        .. availability:: EGL 1.3

    .. py:attribute:: VG_COLORSPACE

        The colorspace used by OpenVG (a value from :py:class:`VGColorspace`).

        .. availability:: EGL 1.3

    .. py:attribute:: WIDTH

        The surface’s width in pixels (an ``int``).


.. py:class:: SurfaceTypeFlag

    Surfaces that may be supported by a configuration. Despite the name, this
    includes both surface types (the first three flags below) and available
    surface attributes.

    .. availability:: EGL 1.0

    .. py:attribute:: NONE
    
        No particular surface is supported.

    .. py:attribute:: PBUFFER

        Pbuffer surfaces are supported. The longer form :py:attr:`PBUFFER_BIT`
        is provided as an alias.

    .. py:attribute:: PIXMAP

        Pixmap surfaces are supported. The longer form :py:attr:`PIXMAP_BIT` is
        provided as an alias.

    .. py:attribute:: WINDOW

        Window surfaces are supported. The longer form :py:attr:`WINDOW_BIT` is
        provided as an alias.

    .. py:attribute:: MULTISAMPLE_RESOLVE_BOX

        Box-filtered multisample resolve is supported. The longer form
        :py:attr:`MULTISAMPLE_RESOLVE_BOX_BIT` is provided as an alias.

        .. availability:: EGL 1.4

    .. py:attribute:: SWAP_BEHAVIOUR_PRESERVED

        Setting swap behavior to preserve color buffers is supported. The
        longer form :py:attr:`SWAP_BEHAVIOUR_PRESERVED_BIT` is provided as an
        alias.

        .. availability:: EGL 1.4

    .. py:attribute:: VG_ALPHA_FORMAT_PRE

        OpenVG rendering with premultiplied alpha is supported. The longer form
        :py:attr:`VG_ALPHA_FORMAT_PRE_BIT` is provided as an alias.

        .. availability:: EGL 1.3

    .. py:attribute:: VG_COLORSPACE_LINEAR

        OpenVG rendering in linear colorspace is supported. The longer form
        :py:attr:`VG_COLORSPACE_LINEAR_BIT` is provided as an alias.

        .. availability:: EGL 1.3


.. py:class:: SwapBehavior

    Possible effects on the color buffer when a buffer swap is performed.

    .. availability:: EGL 1.2

    .. py:attribute:: BUFFER_DESTROYED

        The contents of the color buffer may be destroyed or changed when a
        buffer swap is performed.

    .. py:attribute:: BUFFER_PRESERVED

        The contents of the color buffer are preserved when a buffer swap is
        performed.


.. py:class:: SyncAttrib

    Attributes that may be specified when creating a sync object.

    .. availability:: EGL 1.5

    .. py:attribute:: CL_EVENT_HANDLE

        An OpenCL event handle.


.. py:class:: SyncCondition

    Conditions that can cause a sync object to be signaled.

    .. availability:: EGL 1.5

    .. py:attribute:: PRIOR_COMMANDS_COMPLETE

        The sync object is signaled when all commands issued prior to its
        creation are complete. The longer form
        :py:attr:`SYNC_PRIOR_COMMANDS_COMPLETE` is provided as an alias.

    .. py:attribute:: CL_EVENT_COMPLETE

        The sync object is signaled when the corresponding OpenCL event is
        complete. The longer form :py:attr:`SYNC_CL_EVENT_COMPLETE` is provided
        as an alias.


.. py:class:: SyncFlag

    Flags that define the waiting behavior of a sync object.

    .. availability:: EGL 1.5
    
    .. py:attribute:: NONE
    
        No particular behavior is called for.

    .. py:attribute:: FLUSH_COMMANDS

        Perform a flush operation (as defined by the client API for the current
        context) before blocking. The longer form
        :py:attr:`SYNC_FLUSH_COMMANDS_BIT` is provided as an alias.


.. py:class:: SyncResult

    Results from waiting on a sync object.

    .. availability:: EGL 1.5

    .. py:attribute:: CONDITION_SATISFIED

        The sync object’s condition was satisfied, causing it to become
        signaled. This includes the case where the sync had already been
        signaled before it was waited on.

    .. py:attribute:: TIMEOUT_EXPIRED

        The given timeout expired before the sync object became signaled.


.. py:class:: SyncType

    Available types of sync object.

    .. availability:: EGL 1.5

    .. py:attribute:: FENCE

        A “fence” sync object, which sets a boundary between commands issued
        before it was created and those issued after it was created. The longer form :py:attr:`SYNC_FENCE` is provided as an alias.

    .. py:attribute:: CL_EVENT

        A CL event sync object, which waits on the completion of an event
        defined in OpenCL. The longer form :py:attr:`SYNC_CL_EVENT` is provided
        as an alias.


.. py:class:: TextureFormat

    Formats for the OpenGL ES texture created when binding a pbuffer surface as
    a texture.

    .. availability:: EGL 1.1

    .. py:attribute:: NO_TEXTURE

        Binding as a texture is not allowed.

    .. py:attribute:: RGB

        An RGB texture will be created. The longer form :py:attr:`TEXTURE_RGB`
        is provided as an alias.

    .. py:attribute:: RGBA

         An RGBA texture will be created. The longer form
         :py:attr:`TEXTURE_RGBA` is provided as an alias.


.. py:class:: TextureTarget

    The target for the OpenGL texture created when binding a pbuffer surface as
    a texture.

    .. availability:: EGL 1.1

    .. py:attribute:: NO_TEXTURE

        Binding as a texture is not allowed.

    .. py:attribute:: TEXTURE_2D

        The created texture will be bound to the ``TEXTURE_2D`` target. (While
        a short name of ``2D`` would be consistent, it would not be a valid
        identifier.)


.. py:class:: TransparentType

    Transparency types that may be supported.

    .. availability:: EGL 1.0

    .. py:attribute:: NONE

        Transparency is not supported.

    .. py:attribute:: RGB

        Indexed transparency is supported (a specific set of red, green, and
        blue values will be treated as transparent). The longer form
        :py:attr:`TRANSPARENT_RGB` is provided as an alias.


.. py:class:: VGAlphaFormat

    OpenVG alpha formats that a surface may use.

    .. availability:: EGL 1.3

    .. py:attribute:: NONPRE

        RGB values are not premultiplied by the alpha value. The longer form
        :py:attr:`VG_ALPHA_FORMAT_NONPRE` is provided as an alias.

    .. py:attribute:: PRE

        RGB values are premultiplied by the alpha value. The longer form :py:attr:`VG_ALPHA_FORMAT_PRE` is provided as an alias.


.. py:class:: VGColorspace

    Colorspaces supported by OpenVG.

    .. availability:: EGL 1.3

    .. py:attribute:: LINEAR

        A linear RGB colorspace. The longer form
        :py:attr:`VG_COLORSPACE_LINEAR` is provided as an alias.

    .. py:attribute:: sRGB

        The sRGB non-linear, perceptually uniform colorspace. The longer form :py:attr:`VG_COLORSPACE_sRGB` is provided as an alias.

        Note that unlike :py:class:`GLColorspace`, “sRGB” is here written with
        a lower-case S. To avoid hard-to-detect errors, short and long aliases
        with the capital S are also provided.
