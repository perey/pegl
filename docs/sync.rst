==================
Rendering Contexts
==================

.. py:module:: pegl.sync

This module provides functions and objects for basic synchronisation of
rendering operations. More sophisticated synchronisation capabilities may be
provided in extensions and by client APIs.

Sync objects
============

First introduced in extensions to EGL 1.4, the Sync object is part of the core
EGL 1.5 specification. The following classes are only available on that
version.

.. py:class:: Sync

    An object that is "signalled" when a condition is met, allowing users to
    wait for such a condition before proceeding. Users should not instantiate
    this class themselves, but should instead get instances from the
    :py:meth:`Display.create_sync` method.
    
    The EGL function underlying the destructor is ``eglDestroySync``.

    .. py:method:: client_wait_sync(flags: SyncFlag,
                                    timeout: Optional[int]) -> SyncResult

        Block the calling thread until this sync object is signalled, or until
        the given timeout (in nanoseconds) has expired. The return value is
        :py:obj:`SyncResult.CONDITION_SATISFIED` in the former case and
        :py:obj:`SyncResult.TIMEOUT_EXPIRED` in the latter.

        If the ``timeout`` argument is zero, the call returns immediately,
        allowing the current status of the sync condition to be checked without
        waiting. If the ``timeout`` argument is None, the call will wait
        indefinitely. Other timeout values are adjusted to a level of accuracy
        defined by the implementation, which may not be accurate to nanosecond
        precision.
        
        The underlying EGL function is ``eglClientWaitSync``.

    .. py:method:: wait_sync(flags: SyncFlag) -> None

        Instruct the client API implementation to wait until the sync object is
        signalled, without blocking the calling thread.
        
        The underlying EGL function is ``eglWaitSync``.

    .. py:method:: sync_type -> SyncCondition

        A read-only property that gives the condition that will cause this sync
        object to be signalled.
        
        The underlying EGL function is ``eglGetSyncAttrib`` with an
        ``attribute`` value of ``EGL_SYNC_CONDITION``.

    .. py:method:: sync_status -> bool

        A read-only property that checks whether or not the sync object has
        been signalled.
        
        The underlying EGL function is ``eglGetSyncAttrib`` with an
        ``attribute`` value of ``EGL_SYNC_STATUS``.

    .. py:method:: sync_type -> SyncType

        A read-only property that gives the type of this sync object.
        
        The underlying EGL function is ``eglGetSyncAttrib`` with an
        ``attribute`` value of ``EGL_SYNC_TYPE``.

.. py:class:: SyncType

    An enumeration of sync object types.
    
    - SYNC_FENCE (FENCE for short)
    - SYNC_CL_EVENT (CL_EVENT for short)

.. py:class:: SyncAttrib

    An enumeration of sync object attributes.

    - CL_EVENT_HANDLE: an OpenCL event handle

.. py:class:: SyncCondition

    An enumeration of conditions that can cause a sync object to be signalled.

    - SYNC_PRIOR_COMMANDS_COMPLETE (PRIOR_COMMANDS_COMPLETE for short)
    - SYNC_CL_EVENT_COMPLETE (CL_EVENT_COMPLETE for short)

.. py:class:: SyncFlag

    An enumeration of flags that define the waiting behaviour of a sync object.

    - SYNC_FLUSH_COMMANDS_BIT (FLUSH_COMMANDS for short): perform a flush
      operation (as defined by the client API for the current context) before
      blocking.

.. py:class:: SyncResult

    An enumeration of results from waiting on a sync object.

    - CONDITION_SATISFIED
    - TIMEOUT_EXPIRED

Synchronisation functions
=========================

.. py:function:: wait_client() -> None

    Ensure that native rendering operations issued after this function call
    are not executed until any outstanding client API rendering operations
    have completed.

    The underlying EGL function is ``eglWaitClient``.

.. py:function:: wait_gl() -> None

    Ensure that native rendering operations issued after this function call
    are not executed until any outstanding OpenGL ES rendering operations
    have completed. This function is provided for backwards compatibility.

    The underlying EGL function is ``eglWaitClient``.

.. py:function:: wait_native(engine: Optional[NativeEngine]=None) -> None

    Ensure that client API rendering operations issued after this function call
    are not executed until any outstanding native rendering operations
    have completed. If the ``engine`` argument is None or omitted, the "core"
    (default or most common) API for native rendering is assumed.
    
    Calling this function when there is no current context, or when the current
    surface does not allow for native rendering, is still successful.

    The underlying EGL function is ``eglWaitNative``.

..py:class:: NativeEngine

    An enumeration of native drawing APIs (i.e. not those recognised as EGL
    client APIs, namely OpenGL, OpenGL ES, and OpenVG). The core specification
    only provides one value, representing a default or most common native API.
    Extensions may define additional values.
    
    - CORE_NATIVE_ENGINE (CORE for short)