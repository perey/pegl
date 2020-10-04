========
Displays
========

.. py:module:: pegl.display

In EGL, a display both represents a (physical or virtual) display device,
and provides the environment for all other EGL objects and most other
operations. The majority of EGL functionality is provided through methods on
:py:class:`Display` instances or their attributes.

The class and function listed below are defined in the
:py:mod:`pegl.display` module, but are also imported to the top-level
:py:mod:`pegl` namespace.

The Display class
=================

.. py:class:: Display(display_id: Optional[int]=None, init=True)

    A display is both a representation of a (physical or virtual) display, and
    an environment for other EGL objects.

    The ``display_id`` argument is an optional, platform-specific handle to
    a native display object (a ``wl_display`` on Wayland, a ``HDC`` on Windows,
    etc.), handled as a ``void *`` in C and as an ``int`` in Python. If it is
    omitted or ``None``, the default EGL display is used.

    If ``init`` is ``True`` (the default), the display is also initialized,
    just as if its :py:meth:`initialize` method had been called.

    Instances of this class are cached until their destructor is called;
    calling the constructor with the same ``display_id`` will return the same
    object. If the EGL implementation cannot provide a display corresponding
    to the given ``display_id``, then the special object :py:obj:`NoDisplay`
    is returned.

    The EGL functions underlying the constructor are :eglfunc:`eglGetDisplay`
    and, if the ``init`` argument is ``True``, :eglfunc:`eglInitialize`. The
    destructor calls :eglfunc:`eglTerminate` and, if on EGL 1.2 or later,
    :eglfunc:`eglReleaseThread`.

    .. availability::
        EGL 1.0. Passing a ``display_id`` of ``None`` to get a default display
        is available in EGL 1.4.
    
    .. py:method:: get_current_display() -> Display
        :classmethod:

        Get the display to which the current context for the calling thread
        belongs, or :py:obj:`NoDisplay` if no context is bound.

        .. todo::
            Having this here, not on :py:class:`pegl.Context`, is an inconsistency. But my quick-and-dirty move broke all the places
            that call it. I’ll need to consider them and the dependency
            structure more carefully.

        The underlying EGL function is :eglfunc:`eglGetCurrentDisplay`.

    .. py:method::
        get_platform_display(platform: pegl.enums.Platform, native_display: int, attribs: Optional[dict[pegl.enums.DisplayAttrib, Any]]=None, init=True) -> Display
        :classmethod:

        An alternate constructor for a display that takes a platform
        identifier, and allows platform-specific extensions to define what
        the ``native_display`` argument represents. It is generically handled
        as a ``void *`` in C and as an ``int`` in Python, just like the
        ``display_id`` argument to the default constructor.

        This method is only available in EGL 1.5, but is the preferred
        constructor when that version is supported.

        If ``init`` is ``True`` (the default), the display is also initialized,
        just as if its :py:meth:`initialize` method had been called.

        As with the default constructor, instances created by this function are
        cached until their destructor is called, and calling the constructor
        with the same ``platform`` and ``native_display`` will return the same
        object. If the EGL implementation cannot provide a display
        corresponding to the given ``native_display``, then the special object
        :py:obj:`NoDisplay` is returned.

        The underlying EGL functions are :eglfunc:`eglGetPlatformDisplay` and,
        if the ``init`` argument is True, :eglfunc:`eglInitialize`.

        .. availability:: EGL 1.5

    .. py:method::
        choose_config(attribs: dict[pegl.enums.ConfigAttrib, Any], num_config: Optional[int]=None) -> tuple[pegl.config.Config, ...]

        Get a list of configurations available on this display that match the
        requested attributes.

        If the optional ``num_config`` argument is supplied and is not
        ``None``, then it sets the maximum number of configurations that will
        be returned. Otherwise, all matching configurations will be returned,
        as if the value of ``num_config`` was first retrieved using
        :py:meth:`get_config_count`.

        The underlying EGL function is :eglfunc:`eglChooseConfig`.

    .. py:method:: get_config_count() -> int

        Get the number of configurations available on this display.

        The underlying EGL function is :eglfunc:`eglGetConfigs` with a null
        ``configs`` argument.

    .. py:method::
        get_configs(num_config: Optional[int]=None) -> tuple[pegl.config.Config, ...]

        Get a list of configurations available on this display.

        If the optional ``num_config`` argument is supplied and is not
        ``None``, then it sets the maximum number of configurations that will
        be returned. Otherwise, all configurations will be returned, as if
        the value of ``num_config`` was first retrieved using
        :py:meth:`get_config_count`.

        The underlying EGL function is :eglfunc:`eglGetConfigs`.

    .. py:method::
        create_image(target: pegl.enums.ImageTarget, buffer: int, attribs: Optional[dict[pegl.enums.ImageAttrib, Any]]=None) -> pegl.image.Image

        Create an image object from the given buffer. This creates an image
        without reference to a context (which would indicate the relevant
        client API). To create an image using a context, call the
        :py:meth:`~pegl.context.Context.create_image` method of that context
        instead.

        Note that there are no targets defined in the core specification that
        allow image creation without a context. This method is provided to
        support extension use.

        The ``buffer`` argument is a handle to a client buffer. The actual
        type may vary, but it is fundamentally treated as a ``void *`` in C,
        and as an ``int`` in Python.

        The underlying EGL function is :eglfunc:`eglCreateImage`, with a
        ``ctx`` argument of ``EGL_NO_CONTEXT``.

        .. availability:: EGL 1.5

    .. py:method::
        create_sync(synctype: pegl.enums.SyncType, attribs: Optional[dict[pegl.enums.SyncAttrib, Any]]) -> pegl.sync.Sync

        Create a sync object with the given attributes. Available types are
        the fence sync (which takes no attributes) and the OpenCL event sync
        (which needs an OpenCL event handle).

        The underlying function is :eglfunc:`eglCreateSync`.

        .. availability:: EGL 1.5

    .. py:method:: initialize() -> tuple[int, int]

        Initialize this display, and by extension, the EGL environment that it
        provides. Initialization is done by the constructor unless the ``init``
        argument was ``False``. Calling this function again is allowed, but has
        no effect.

        The version number of the EGL implementation is returned as a tuple
        ``(major, minor)``. The same information is available from the
        :py:attr:`version` property.

        The underlying EGL function is :eglfunc:`eglInitialize`.

    .. py:method:: terminate() -> None

        Terminate all resources associated with this display. The display
        itself remains valid, but it must be re-initialized by calling its
        :py:meth:`initialize` method.

        The underlying EGL function is :eglfunc:`eglTerminate`.

    .. py:method:: attribs() -> dict[pegl.enums.DisplayAttrib, int]
        :property:

        A (possibly empty) mapping of attributes to values. Read-only.
        
        This is populated by the alternate constructor
        :py:meth:`get_platform_display` and is empty if the display was not
        created by that function.

        .. availability::
            Provided on all versions, but only populated on EGL 1.5 when
            :py:meth:`get_platform_display` is used.

    .. py:method:: client_apis() -> str
        :property:

        A space-separated list of client APIs supported by the EGL
        implementation on this display. Read-only.
        
        The supported APIs will always include at least one of ``OpenGL``,
        ``OpenGL_ES``, or ``OpenVG``.

        The underlying EGL function is :eglfunc:`eglQueryString` with ``name``
        ``EGL_CLIENT_APIS``.

        .. availability:: EGL 1.2

    .. py:method:: extensions() -> str
        :property:

        A space-separated list of EGL extensions supported by the EGL
        implementation on this display. Read-only.

        The underlying EGL function is :eglfunc:`eglQueryString` with ``name``
        ``EGL_EXTENSIONS``.

    .. py:method:: swap_interval() -> int
        :property:

        The minimum interval between buffer swaps, in video frames.

        Note that while this is a property of the display, there must be a
        currently bound context and surface in the calling thread, and the
        maximum and minimum values for this property are defined by the
        configuration that was used to create that context. Values outside that
        range are not an error, but are silently clamped.
        
        A value of 0 means that rendering operations will be shown immediately.

        The underlying EGL function for the setter is
        :eglfunc:`eglSwapInterval`. When getting this property, its value is
        not queried from the EGL implementation; instead, it is set to the
        default value of 1 to begin with, and is then recorded whenever the
        property is set. This means it **will not** reflect the actual value
        used when attempting to set a swap interval that it out of the bounds
        allowed by the configuration.

        .. availability:: EGL 1.1

    .. py:method:: vendor() -> str
        :property:

        The vendor information for the EGL implementation. Read-only.

        The underlying EGL function is :eglfunc:`eglQueryString` with ``name``
        ``EGL_VENDOR``.

    .. py:method:: version() -> tuple[int, int, str]
        :property:

        The major and minor version numbers, and any vendor-specific version
        information, for the EGL implementation. Read-only.

        The underlying EGL function is :eglfunc:`eglQueryString` with ``name``
        ``EGL_VERSION``.

    .. py:method:: version_string() -> str
        :property:

        The version information for the EGL implementation from which this display was obtained. Read-only.
        
        This is the same information as the :py:attr:`version` property, but
        this property does not attempt to parse the string.

        The underlying EGL function is :eglfunc:`eglQueryString` with ``name``
        ``EGL_VERSION``.

.. py:data:: NoDisplay(Display)

    An instance of :py:class:`Display` that is not bound to any physical or
    virtual display. It can be used to query aspects of the EGL implementation,
    and is also returned when an attempt to create a :py:class:`Display`
    instance cannot be matched to an available display.

    The :py:attr:`~Display.extensions`, :py:attr:`~Display.version`, and
    :py:attr:`~Display.version_string` properties are valid on this instance,
    but other properties and methods are not.

    .. availability::
        EGL 1.0. Getting the :py:attr:`~Display.extensions` property is first
        allowed in extensions to EGL 1.4, and is core in EGL 1.5. Getting the
        :py:attr:`~Display.version` property was allowed in a revision of EGL
        1.5.

Other functions
===============

While not strictly related to displays, the :py:func:`release_thread` function
is provided here, as it is relevant to the overall EGL environment (at least
on a per-thread level).

.. py:function:: release_thread() -> None

    Clear all per-thread state held by EGL for the current thread. This should
    generally be called after a :py:class:`Display` object is finalized, to
    complete the clean-up of allocated resources. It may also be called at
    other times.

    The underlying EGL function is :eglfunc:`eglReleaseThread`.

    .. availability:: EGL 1.2
