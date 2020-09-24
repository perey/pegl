===============
Display Objects
===============

.. py:module:: pegl.display

This module provides the :py:class:`Display` class. Instances of this class
not only represent a (physical or virtual) display device, but also provide
the environment for all other EGL objects and most other operations. The
majority of EGL functionality is provided through methods on
:py:class:`Display` instances or their attributes.

Displays
========

.. py:class:: Display(display_id: Optional[int]=None, init=True)

    A display object is both a representation of a (physical or virtual)
    display, and an environment for other objects.

    The ``display_id`` argument is an optional, platform-specific handle to
    a native display object (a ``wl_display`` on Wayland, a ``HDC`` on Windows,
    etc.), handled as a ``void *`` in C and as an ``int`` in Python. If it is
    omitted or None, the default EGL display object is used.

    If ``init`` is True (the default), the display object is also initialised,
    just as if its :py:meth:`initialize` method had been called.

    Instances of this class are cached until their destructor is called;
    calling the constructor with the same ``display_id`` will return the same
    object. If the EGL implementation cannot provide a display corresponding
    to the given ``display_id``, then the special object :py:obj:`NoDisplay`
    is returned.

    The EGL functions underlying the constructor are ``eglGetDisplay`` and,
    if the ``init`` argument is True, ``eglInitialize``. The destructor calls ``eglTerminate``.

    .. py:method:: get_platform_display(platform: Platform,
                                        native_display: int,
                                        init=True) -> Display

        :classmethod:

        An alternate constructor for a display object that takes a platform
        identifier, and allows platform-specific extensions to define what
        the ``native_display`` argument represents. It is generically handled
        as a ``void *`` in C and as an ``int`` in Python, just like the
        ``display_id`` argument to the default constructor.

        This method is only available in EGL 1.5, but is the preferred
        constructor when that version is supported.

        If ``init`` is True (the default), the display object is also
        initialised, just as if its :py:meth:`initialize` method had been
        called.

        As with the default constructor, instances created by this function are
        cached until their destructor is called, and calling the constructor
        with the same ``platform`` and ``native_display`` will return the same
        object. If the EGL implementation cannot provide a display
        corresponding to the given ``native_display``, then the special object
        :py:obj:`NoDisplay` is returned.

        The underlying EGL functions are ``eglGetPlatformDisplay`` and,
        if the ``init`` argument is True, ``eglInitialize``.

    .. py:method:: choose_config(attribs: Dict[ConfigAttrib, Any],
                                 num_configs: Optional[int]=None)
                       -> Tuple[Config, ...]

        Get a list of configurations available on this display object that
        match the requested attributes.

        If the optional ``num_configs`` argument is supplied and is not None,
        then it sets the maximum number of configurations that will be
        returned. Otherwise, all matching configurations will be returned, as
        if the value of ``max_configs`` was first retrieved using
        :py:meth:`get_config_count`.

        The underlying EGL function is ``eglChooseConfigs``.

    .. py:method:: get_config_count() -> int

        Get the number of configurations available on this display object.

        The underlying EGL function is ``eglGetConfigs`` with a null
        ``configs`` argument.

    .. py:method:: get_configs(max_configs: Optional[int]=None)
                       -> Tuple[Config, ...]

        Get a list of configurations available on this display object.

        If the optional ``num_configs`` argument is supplied and is not None,
        then it sets the maximum number of configurations that will be
        returned. Otherwise, all configurations will be returned, as if
        the value of ``max_configs`` was first retrieved using
        :py:meth:`get_config_count`.

        The underlying EGL function is ``eglGetConfigs``.

    .. py:method:: create_image(target: ImageTarget, buffer: int,
                                attribs: Optional[Dict[ImageAttrib, Any]]=None)
                       -> Image

        Create an image object from the given buffer. This creates an image
        without reference to a context (which would indicate the relevant
        client API). To create an image using a context, call the
        py:meth:`Context.create_image` method of that context instead.

        The ``buffer`` argument is a handle to a client buffer. The actual
        type may vary, but it is fundamentally treated as a ``void *`` in C,
        and as an ``int`` in Python.

        This method is only available in EGL 1.5. Note that no targets
        defined in the core specification allow image creation without a
        context. This method is provided to support extension use.

        The underlying EGL function is ``eglCreateImage``, with a ``ctx``
        argument of ``EGL_NO_CONTEXT``.

    .. py:method:: create_sync(synctype: SyncType,
                               attribs: Optional[Dict[SyncAttrib, Any]])
                       -> Sync

        Create a sync object with the given attributes. Available types are
        the fence sync (which takes no attributes) and the OpenCL event sync
        (which needs an OpenCL event handle).

        This method is only available in EGL 1.5.

        The underlying function is ``eglCreateSync``.

    .. py:method:: initialize() -> None

        Initialise this display object, and by extension, the EGL environment
        that it provides. Initialisation is done by the constructor unless
        the ``init`` argument was False. Calling this function again is
        allowed, but has no effect.

        The display object's py:meth:`version` property is updated when this
        method is called (or when the constructor initialises the object). It
        is None when the display object has not been initialised.

        The underlying EGL function is ``eglInitialize``.

    .. py:method:: terminate() -> None

        Terminate all resources associated with this display. The display
        itself remains valid, but it must be re-initialised by calling its
        :py:meth:`initialize` method.

        The underlying EGL function is ``eglTerminate``.

    .. py:method:: attribs -> Dict[Attrib, int]

        :property:

        A read-only property giving a (possibly empty) mapping of attributes to
        values. This is populated by the alternate constructor
        :py:meth:`get_platform_display` and is empty if the display object was
        not created by that function.

    .. py:method:: client_apis -> str

        :property:

        A read-only property giving a space-separated list of client APIs
        supported by the EGL implementation on this display. It will always
        include at least one of ``OpenGL``, ``OpenGL_ES``, or ``OpenVG``.

        The underlying EGL function is ``eglQueryString`` with ``name``
        ``EGL_CLIENT_APIS``.

    .. py:method:: extensions -> str

        :property:

        A read-only property giving a space-separated list of EGL extensions
        supported by the EGL implementation on this display.

        The underlying EGL function is ``eglQueryString`` with ``name``
        ``EGL_EXTENSIONS``.

    .. py:method:: swap_interval -> int

        :property:

        A write-only property that sets the (minimum) interval between buffer
        swaps, in video frames. Note that while this is a property of the
        display, there must be a currently bound context and surface in the
        calling thread, and the maximum and minimum values for this property
        are defined by the configuration that was used to create that context.
        Values outside that range are not an error, but are silently clamped.

        The underlying EGL function is ``eglSwapInterval``.

    .. py:method:: version -> Tuple(int, int, str)

        :property:

        A read-only property giving the major and minor version numbers, and
        any vendor-specific information, for the EGL implementation from which
        this display was obtained.

        The underlying EGL function is ``eglQueryString`` with ``name``
        ``EGL_VERSION``.

.. py:object:: NoDisplay(Display)

    An instance of :py:class:`Display` that is not bound to any physical or
    virtual display. It can be used to query aspects of the EGL implementation,
    and is also returned when an attempt to create a display object cannot be
    matched to an available display.

    The :py:meth:`extensions` and :py:meth:`version` properties are available
    on this instance, but other properties and methods are not.

Other functions
===============

While not strictly related to displays, the :py:func:`release_thread` function
is provided here, as it is relevant to the overall EGL environment (at least
on a per-thread level).

.. py:function:: release_thread() -> None

    Clear all per-thread state held by EGL for the current thread. This should
    generally be called after a :py:class:`Display` object is finalised, to
    complete the clean-up of allocated resources. It may also be called at
    other times.

    TODO: The older version of pegl included this in the Display destructor.
    Shall I put it back in?

    The underlying EGL function is ``eglReleaseThread``.
