==================
Rendering contexts
==================

.. py:module:: pegl.context

An EGL rendering context is an implicit state that affects how client APIs are
to perform draw and read operations. As it is implicit, a :py:class:`Context`
instance is made current in a thread, and is then used for subsequent rendering
operations in that thread until another context (or no context) is made
current.

The class and functions listed below are defined in the
:py:mod:`pegl.context` module, but are also imported to the top-level
:py:mod:`pegl` namespace.

The Context class
=================

.. py:class:: Context

    A context encapsulates per-thread state that affects how client APIs are to
    perform draw and read operations. Users should not instantiate this class
    themselves, but should instead get instances from the
    :py:meth:`~pegl.config.Config.create_context` method of a
    :py:class:`pegl.config.Config` instance.

    Instances of this class are cached until their destructor is called, so
    that they can be retrieved by calling :py:meth:`get_current_context`.
    
    Note that all properties on :py:class:`Context` instances are read-only.

    The EGL function underlying the destructor is :eglfunc:`eglDestroyContext`.

    .. availability:: EGL 1.0

    .. py:method:: get_current_context() -> Optional[Context]
        :classmethod:

        Get the context that is current for this thread, or ``None`` if no
        context (or no client API) is bound.

        The underlying EGL function is :eglfunc:`eglGetCurrentContext`.

        .. availability:: EGL 1.4

    .. py:method::
        get_current_surface(readdraw: pegl.enums.ReadOrDraw) -> Optional[pegl.surface.Surface]
        :classmethod:

        Get the surface bound to the current context in the calling thread for
        either reading or drawing, or ``None`` if no surface is bound. This
        method is an alternative to the :py:attr:`current_draw_surface` and
        :py:attr:`current_read_surface` properties.

        The underlying EGL function is :eglfunc:`eglGetCurrentSurface`.

    .. py:method:: current_draw_surface() -> Optional[pegl.surface.Surface]
        :classmethod:
        :property:

        The surface bound to the current context for drawing, or ``None`` if no
        surface is bound.

        The underlying EGL function is :eglfunc:`eglGetCurrentSurface` with a
        ``readdraw`` argument of ``EGL_DRAW``.

    .. py:method:: current_read_surface() -> Optional[pegl.surface.Surface]
        :classmethod:
        :property:

        The surface bound to the current context for reading, or ``None`` if no
        surface is bound.

        The underlying EGL function is :eglfunc:`eglGetCurrentSurface` with a
        ``readdraw`` argument of ``EGL_READ``.

    .. py:method:: release_current() -> None
        :classmethod:

        Release the current context for the calling thread, without binding
        another one.

        The underlying EGL function is :eglfunc:`eglMakeCurrent`, with a
        ``ctx`` argument of ``EGL_NO_CONTEXT``.

    .. py:method::
        create_image(target: pegl.enums.ImageTarget, buffer: int, attribs: Optional[dict[pegl.enums.ImageAttrib, Any]]=None) -> Image

        Create an image from the given buffer.

        The ``buffer`` argument is a handle to a client buffer. The actual
        type may vary, but it is fundamentally treated as a ``void *`` in C,
        and as an ``int`` in Python.

        The underlying EGL function is :eglfunc:`eglCreateImage`.

        .. availability:: EGL 1.5

    .. py:method::
        make_current(draw: Optional[pegl.surface.Surface]=None, read: Optional[pegl.surface.Surface]=None) -> None

        Make this context current for the calling thread, and bind the given
        surfaces to it for drawing and reading. If no surfaces are specified,
        the context is made current without any bound surfaces.

        It is not possible to bind a surface for one operation and no surface
        for the other, so if only one surface is specified, it will be bound
        for both drawing and reading. Note that binding the same surface for
        drawing and reading is compulsory for OpenVG, so specifying the surface
        just once is recommended in this case.

        The underlying EGL function is :eglfunc:`eglMakeCurrent`.

    .. py:method:: client_type() -> pegl.enums.ClientAPI
        :property:

        The client API that this context supports.

        The underlying EGL function is :eglfunc:`eglQueryContext` with an
        ``attribute`` value of ``EGL_CONTEXT_CLIENT_TYPE``.

        .. availability:: EGL 1.2

    .. py:method:: client_version() -> int
        :property:

        The major version of the client API (only meaningful for OpenGL ES)
        that this context actually supports, which may differ from the one
        requested when it was created.

        For consistency with context creation, :py:attr:`major_version` is
        provided as an alias of this property.

        The underlying EGL function is :eglfunc:`eglQueryContext` with an
        ``attribute`` value of ``EGL_CONTEXT_CLIENT_VERSION``.

        .. availability:: EGL 1.3

    .. py:method:: config() -> pegl.config.Config
        :property:

        The configuration used to create this context.

        The underlying EGL function is :eglfunc:`eglQueryContext` with an
        ``attribute`` value of ``EGL_CONFIG_ID``.

    .. py:method:: config_id() -> int
        :property:

        The unique identifier of the configuration used to create this context.
        
        For most users, the :py:attr:`config` property will be more useful.

        The underlying EGL function is :eglfunc:`eglQueryContext` with an
        ``attribute`` value of ``EGL_CONFIG_ID``.

    .. py:method:: render_buffer() -> Optional[pegl.enums.RenderBuffer]
        :property:

        The buffer that client APIs using this context will render to. The
        result depends both on the context and on the surface bound to it for
        drawing. If no surface is bound, the result is ``None``.

        Note that client APIs may be able to override this value, and in that
        event the value will not reflect the actual buffer used.

        The underlying EGL function is :eglfunc:`eglQueryContext` with an
        ``attribute`` value of ``EGL_RENDER_BUFFER``.

        .. availability:: EGL 1.2

Other functions
===============

.. py:function:: bind_api(api: pegl.enums.ClientAPI) -> None

    Bind the given client API as the current renderer for this thread.

    The underlying EGL function is :eglfunc:`eglBindAPI`.

    .. availability:: EGL 1.2

.. py:function:: query_api() -> Optional[pegl.enums.ClientAPI]

    Get the client API that is bound as the current renderer for this thread.
    The default is OpenGL ES (:py:obj:`.ClientAPI.OPENGL_ES`), unless that is
    unsupported, in which case the default is ``None``.

    The underlying EGL function is :eglfunc:`eglQueryAPI`.

    .. availability:: EGL 1.2
