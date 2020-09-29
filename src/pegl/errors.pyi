"""Typing stubs for pegl.errors"""

EGL_SUCCESS: int
EGL_NOT_INITIALIZED: int
EGL_BAD_ACCESS: int
EGL_BAD_ALLOC: int
EGL_BAD_ATTRIBUTE: int
EGL_BAD_CONFIG: int
EGL_BAD_CONTEXT: int
EGL_BAD_CURRENT_SURFACE: int
EGL_BAD_DISPLAY: int
EGL_BAD_MATCH: int
EGL_BAD_NATIVE_PIXMAP: int
EGL_BAD_NATIVE_WINDOW: int
EGL_BAD_PARAMETER: int
EGL_BAD_SURFACE: int
EGL_CONTEXT_LOST: int

class EGLError(Exception): ...

class NotInitializedError(EGLError): ...

class BadAccessError(EGLError): ...

class BadAllocError(EGLError): ...

class BadAttributeError(EGLError): ...

class BadConfigError(EGLError): ...

class BadContextError(EGLError): ...

class BadCurrentSurfaceError(EGLError): ...

class BadDisplayError(EGLError): ...

class BadMatchError(EGLError): ...

class BadNativePixmapError(EGLError): ...

class BadNativeWindowError(EGLError): ...

class BadParameterError(EGLError): ...

class BadSurfaceError(EGLError): ...

class ContextLostError(EGLError): ...

KNOWN_ERRORS: dict[int, EGLError]
