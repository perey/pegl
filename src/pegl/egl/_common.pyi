"""Typing stubs for pegl.egl._common"""

# Standard library imports.
import ctypes
from enum import IntFlag
from typing import Any, Callable, ClassVar, List, Optional, Sequence, Type

__all__: List[str] = ...

EGLBoolean           = ctypes.c_bool
EGLConfig            = ctypes.c_void_p
EGLConfig_p          = ctypes.POINTER(EGLConfig)
EGLContext           = ctypes.c_void_p
EGLDisplay           = ctypes.c_void_p
EGLNativeDisplayType = ctypes.c_void_p
EGLNativePixmapType  = ctypes.c_void_p
EGLNativeWindowType  = ctypes.c_void_p
EGLSurface           = ctypes.c_void_p
EGLint               = ctypes.c_int32
EGLint_p             = ctypes.POINTER(EGLint)
EGLClientBuffer      = ctypes.c_void_p
EGLenum              = ctypes.c_uint
EGLAttrib            = ctypes.c_ssize_t
EGLAttrib_p          = ctypes.POINTER(EGLAttrib)
EGLImage             = ctypes.c_void_p
EGLSync              = ctypes.c_void_p
EGLTime              = ctypes.c_uint64

def eglGetError() -> EGLint: ...

def eglGetProcAddress(procname: ctypes.c_char_p) -> ctypes.c_void_p: ...

class Arg(IntFlag):
    IN: ClassVar[Arg] = ...
    OUT: ClassVar[Arg] = ...
    INOUT: ClassVar[Arg] = ...
    IN_DEFAULT0: ClassVar[Arg] = ...
    

def _load_function(func_name: str, restype: Any, *args: Any,
                   **kwargs: Any) -> Callable: ...
