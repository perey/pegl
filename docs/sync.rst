===============
Synchronization
===============

.. py:module:: pegl.sync

Rendering operations are generally an asynchronous process—commands may be
completed in any order. For situations where order is significant, EGL provides
simple synchronization functions and objects.

The class and functions listed below are defined in the :py:mod:`pegl.sync`
module, but are also imported to the top-level :py:mod:`pegl` namespace.

The Sync class
==============

.. py:class:: Sync

    An object that is “signaled” when a condition is met, allowing users to
    wait for such a condition before proceeding. Users should not instantiate
    this class themselves, but should instead get instances from the
    :py:meth:`Display.create_sync` method.

    .. availability:: EGL 1.5
    
    The EGL function underlying the destructor is :eglfunc:`eglDestroySync`.

    .. py:method::
        client_wait_sync(flags: pegl.enums.SyncFlag, timeout: Optional[int]) -> pegl.enums.SyncResult

        Block the calling thread until this sync object is signaled, or until
        the given timeout (in nanoseconds) has expired. The return value is
        :py:obj:`~pegl.enums.SyncResult.CONDITION_SATISFIED` in the former case
        and :py:obj:`~pegl.enums.SyncResult.TIMEOUT_EXPIRED` in the latter.

        If the ``timeout`` argument is zero, the call returns immediately,
        allowing the current status of the sync condition to be checked without
        waiting. If the ``timeout`` argument is ``None``, the call will wait
        indefinitely. Other timeout values are adjusted to a level of accuracy
        defined by the implementation, which may not be at nanosecond
        resolution.
        
        The underlying EGL function is :eglfunc:`eglClientWaitSync`.

    .. py:method:: wait_sync(flags: pegl.enums.SyncFlag) -> None

        Instruct the client API implementation to wait until the sync object is
        signaled, without blocking the calling thread.
        
        The underlying EGL function is :eglfunc:`eglWaitSync`.

    .. py:method:: sync_condition -> pegl.enums.SyncCondition

        The condition that will cause this sync object to be signaled.
        Read-only.
        
        The underlying EGL function is :eglfunc:`eglGetSyncAttrib` with an
        ``attribute`` of ``EGL_SYNC_CONDITION``.

    .. py:method:: sync_status -> bool

        Whether or not the sync object has been signaled. Read-only.
        
        The underlying EGL function is :eglfunc:`eglGetSyncAttrib` with an
        ``attribute`` of ``EGL_SYNC_STATUS``.

    .. py:method:: sync_type -> pegl.enums.SyncType

        The type of this sync object. Read-only.
        
        The underlying EGL function is :eglfunc:`eglGetSyncAttrib` with an
        ``attribute`` value of ``EGL_SYNC_TYPE``.

Other functions
===============

.. py:function:: wait_client() -> None

    Ensure that native rendering operations issued after this function call
    are not executed until any outstanding rendering operations from the
    current client API have completed.

    The underlying EGL function is :eglfunc:`eglWaitClient`.

    .. availability:: EGL 1.2

.. py:function:: wait_gl() -> None

    Ensure that native rendering operations issued after this function call
    are not executed until any outstanding OpenGL ES rendering operations
    have completed.
    
    Under EGL 1.2 and later, this is equivalent to saving the currently bound
    API, binding OpenGL ES, calling :py:func:`wait_client`, and then restoring
    the previous API binding.

    The underlying EGL function is :eglfunc:`eglWaitGL`.

    .. availability:: EGL 1.0

.. py:function::
    wait_native(engine: Optional[pegl.enums.NativeEngine]=pegl.enums.NativeEngine.CORE) -> None

    Ensure that client API rendering operations issued after this function call
    are not executed until any outstanding native rendering operations
    have completed.
    
    Calling this function when there is no current context, or when the current
    surface does not allow for native rendering, is still successful.

    The underlying EGL function is :eglfunc:`eglWaitNative`.

    .. availability:: EGL 1.0
