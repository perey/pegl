==================
Rendering Contexts
==================

.. py:module:: pegl.context

This module provides functions and objects related to the rendering context,
including the :py:class:`Context` class. Instances of this class, which are obtained from :py:class:`Config` instances, represent per-thread state that
affects how client APIs are to perform draw and read operations.

Contexts
========

.. py:class:: Context

    A context encapsulates per-thread state that affects how client APIs are to
    perform draw and read operations. Users should not instantiate this class
    themselves, but should instead get instances from the
    :py:meth:`Config.create_context` method.

    Instances of this class are cached until their destructor is called, so
    that they can be retrieved by calling :py:meth:`get_current_context`.

    The EGL function underlying the destructor is ``eglDestroyContext``.

    .. py:method:: get_current_surface(readdraw: ReadOrDraw)
                       -> Optional[Surface]

        Get the surface currently bound to this context for either reading
        or drawing, or None if no surface is bound. This method is an
        alternative to the :py:meth:`draw_surface` and :py:meth:`read_surface`
        properties.

        The underlying EGL function is ``eglGetCurrentSurface``.

    .. py:method:: make_current(draw: Optional[Surface]=None,
                                read: Optional[Surface]=None) -> None

        Make this context current for the thread from which the method is
        called, and bind the given surfaces to it for drawing and reading.

        It is not possible to bind no surface for one operation, so if only one
        surface is specified, it will be bound for both drawing and reading.
        Note that binding the same surface for drawing and reading is
        compulsory for OpenVG, so specifying just one surface is recommended in
        this case.

        The underlying EGL function is ``eglMakeCurrent``.

    .. py:method:: release_current() -> None

        :classmethod:

        Release the current context for the given thread, without binding
        another one.

        The underlying EGL function is ``eglMakeCurrent``, with a ``ctx``
        argument of ``EGL_NO_CONTEXT``.

    .. py:method:: create_image(target: ImageTarget, buffer: int,
                                attribs: Optional[Dict[ImageAttrib, Any]]=None)
                       -> Image

        Create an image object from the given buffer.

        The ``buffer`` argument is a handle to a client buffer. The actual
        type may vary, but it is fundamentally treated as a ``void *`` in C,
        and as an ``int`` in Python.

        This method is only available in EGL 1.5.

        The underlying EGL function is ``eglCreateImage``.

    .. py:method:: client_version -> int

        :property:

        A read-only property giving the major version of the client API
        (only meaningful for OpenGL ES) that this context actually supports,
        which may differ from the one requested when it was created.

        For consistency with context creation, ``major_version`` is provided
        as an alias of this property.

        The underlying EGL function is ``eglQueryContext`` with an
        ``attribute`` value of ``EGL_CONTEXT_CLIENT_VERSION``.

    .. py:method:: config -> Config

        :property:

        A read-only property giving the configuration used to create this
        context.

        The underlying EGL function is ``eglQueryContext`` with an
        ``attribute`` value of ``EGL_CONFIG_ID``.

    .. py:method:: config_id -> int

        :property:

        A read-only property giving the unique identifier of the configuration
        used to create this context. Note that in most cases it will be more
        useful to use the :py:meth:`config` property instead.

        The underlying EGL function is ``eglQueryContext`` with an
        ``attribute`` value of ``EGL_CONFIG_ID``.

    .. py:method:: draw_surface -> Optional[Surface]

        :property:

        A read-only property giving the surface currently bound to this context
        for drawing, or None if no surface is bound.

        The underlying EGL function is ``eglGetCurrentSurface`` with a
        ``readdraw`` argument of ``EGL_DRAW``.

    .. py:method:: read_surface -> Optional[Surface]

        :property:

        A read-only property giving the surface currently bound to this context
        for reading, or None if no surface is bound.

        The underlying EGL function is ``eglQueryContext`` with an
        ``attribute`` value of ``EGL_READ``.

    .. py:method:: render_buffer -> Optional[RenderBuffer]

        :property:

        A read-only property giving the buffer that client APIs using this
        context will render to. The result depends both on the context and on
        the surface bound to it for drawing. If no surface is bound, the result
        is None.

        Note that client APIs may be able to override this value, and in that
        event the value will not reflect the actual buffer used.

        The underlying EGL function is ``eglGetCurrentSurface`` with a
        ``readdraw`` argument of ``EGL_RENDER_BUFFER``.

    .. py:method:: swap_interval -> int

        :property:

        A write-only property that sets the (minimum) interval between buffer
        swaps, in video frames. Note that while this is a property of a
        context, the underlying EGL function depends only on the display to
        which this context belongs. There must be *a* currently bound context
        (with a bound surface) in the calling thread, but it need not be *this*
        context.

        An identical property is provided on :py:class:`Display` objects, where
        it belongs. The present property is only provided for convenience and
        because it seems logical for it to exist here.

        The maximum and minimum allowed values for this property are defined by
        the configuration that was used to create the current context (again,
        not necessarily this context). Values outside that range are not an
        error, but are silently clamped.

        The underlying EGL function is ``eglSwapInterval``.

.. py:class:: ContextAttrib

    An enumeration of rendering context attributes. These are used when
    creating a context, queried from an existing context, or both. Many are
    relevant only to specific client APIs.

    TODO: Is there any point providing the query-only ones (everything that
    doesn't start with CONTEXT)? Because they're queried by properties, not
    by use of this enumeration.

    - CONFIG_ID: the unique identifier of the configuration used to create this
      context.
    - CONTEXT_CLIENT_TYPE (CLIENT_TYPE for short): the client API that this
      context supports.
    - CONTEXT_MAJOR_VERSION (MAJOR_VERSION for short, aliases
      CONTEXT_CLIENT_VERSION and CLIENT_VERSION): the major version number
      of the client API requested (on creation) or actually supported (when
      queried). OpenGL and OpenGL ES only for creation; only meaningful for
      OpenGL ES when queried.
    - CONTEXT_MAJOR_VERSION (MINOR_VERSION for short): the minor version number
      of the client API requested. OpenGL and OpenGL ES only.
    - CONTEXT_OPENGL_PROFILE_MASK (OPENGL_PROFILE for short): the client API
      profile requested. OpenGL 3.2 and later only (though it is ignored, not
      an error, on earlier versions).
    - CONTEXT_OPENGL_DEBUG (OPENGL_DEBUG for short): whether or not the context
      must support debugging functionality. OpenGL and OpenGL ES with the
      relevant extension or core functionality only (though it is ignored, not
      an error, when debug contexts are not supported).
    - CONTEXT_OPENGL_FORWARD_COMPATIBLE (OPENGL_FORWARD_COMPATIBLE for short):
      whether or not the context must be forward-compatible. OpenGL 3.0 and
      later only.
    - CONTEXT_OPENGL_ROBUST_ACCESS (OPENGL_ROBUST_ACCESS for short): whether or
      not the context must support robust buffer access. OpenGL and OpenGL ES
      with the relevant extension or core functionality only.
    - CONTEXT_OPENGL_RESET_NOTIFICATION_STRATEGY
      (OPENGL_RESET_NOTIFICATION_STRATEGY for short): the reset notification
      strategy to use when the context supports robust buffer access.
      Specifying this when robust access is not demanded (as above) is not an
      error, but may not in itself result in a context supporting robust buffer
      access. OpenGL and OpenGL ES with the relevant extension or core
      functionality only.
    - RENDER_BUFFER: which buffer client APIs using this context will render
      to. The result depends both on the context and on the surface bound to
      it for drawing.

.. py:class:: OpenGLProfileFlag

    An enumeration of flags for OpenGL profiles.

    - CONTEXT_OPENGL_CORE_PROFILE_BIT (CORE for short)
    - CONTEXT_OPENGL_COMPATIBILITY_PROFILE_BIT (COMPATIBILITY for short)

.. py:class:: ResetNotificationStrategy

    An enumeration of reset notification strategies.

    - NO_RESET_NOTIFICATION
    - LOSE_CONTEXT_ON_RESET

Other functions
===============

.. py:function:: bind_api(api: ClientAPI) -> None

    Bind the given client API as the current renderer for this thread.

    The underlying EGL function is ``eglBindAPI``.

.. py:function:: query_api() -> Optional[ClientAPI]

    Get the client API that is bound as the current renderer for this thread.
    The default is OpenGL ES (:py:obj:`ClientAPI.OPENGL_ES`), unless that is
    unsupported, in which case the default is None.

    TODO: Make this and bind_api a module-level property?

    The underlying EGL function is ``eglQueryAPI``.

.. py:function:: get_current_context() -> Optional[Context]

    Get the context that is current for this thread, or None if no context
    (or no client API) is bound.

    The underlying EGL function is ``eglGetCurrentContext``.

.. py:function:: get_current_display() -> Optional[Display]

    Get the display to which the current context for this thread belongs, or
    :py:obj:`NoDisplay` if no context is bound.

    The underlying EGL function is ``eglGetCurrentDisplay``.

.. py:class:: ClientAPI

    An enumeration of client APIs.

    - OPENGL_API (OPENGL for short)
    - OPENGL_ES_API (OPENGL_ES for short)
    - OPENVG_API (OPENVG for short)

.. py:class:: ReadOrDraw

    An enumeration identifying which bound surface is expected.

    - DRAW
    - READ