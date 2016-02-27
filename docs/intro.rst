============================
Introduction to Pegl and EGL
============================

What is Pegl?
=============

Pegl is a Python binding for the EGL API, written in native Python 3 using the
ctypes_ module in the Python standard library.

.. _ctypes: http://docs.python.org/py3k/library/ctypes

----------------------
Okay, but what is EGL?
----------------------

EGL_ is a specification from the `Khronos Group`_, the consortium that manages
such widely-used cross-platform media APIs as OpenGL. Here’s how the EGL_ site
itself describes EGL:

    EGL™ is an interface between Khronos rendering APIs such as OpenGL ES or
    OpenVG and the underlying native platform window system. It handles
    graphics context management, surface/buffer binding, and rendering
    synchronization and enables high-performance, accelerated, mixed-mode 2D
    and 3D rendering using other Khronos APIs.

This by itself is not the most helpful explanation ever. What follows is
**not** in any way an official description, nor is it written with any input
from anyone in a position to know these things for sure; it’s merely my
piecing together of clues and relationships.

OpenGL has been around for a long time, providing a consistent cross-platform
set of 3D graphics capabilities. What it doesn’t provide, however, are certain
essential setup steps: working with displays (physical or virtual), obtaining
a windowed or full-screen interface for a program, setting options for the
graphics context, and so forth. The mechanics for doing these things remained
platform-specific, but every OpenGL program had to do them somehow… in fact,
so did every graphical application, no matter what graphics API it used.

Different platforms provide their own native APIs for some of these things:
alphabetically, some of the main ones are CGL on OS X, GLX on the X Window
System, and WGL on Microsoft Windows. Already you can start to see what EGL
patterns its name on and get an idea of what it’s for.

Actually, EGL doesn’t really stand for anything. It certainly doesn’t stand
for “Embedded Graphics Layer” or the like. However, it was introduced at about
the same time that OpenGL ES—a version or subset of OpenGL for embedded
systems—was being put forward, so you could be forgiven for thinking that.

Aside from those platform-specific APIs, lots of cross-platform libraries have
been developed to paper over the differences between platforms: GLUT, SDL,
SFML, and more, not to mention OpenGL modules for all the major GUI toolkits
out there. EGL doesn’t *replace* these, although it could underlie them.
Notably, you still need some way of getting a drawing area (windowed or
full-screen) from the system, before you can “bind” an EGL drawing surface to
it. But EGL does take care of many of the functions common to these libraries
and APIs. (A quick scan of function names suggests that it’s most similar to
CGL.)

EGL isn’t just for OpenGL ES. It can work with OpenGL too (although all the
other libraries are pretty entrenched there, so you’ll have a hard time
finding anyone using it for that), and it’s also assumed to be present by
OpenVG, a 2D vector graphics API. Most intriguingly, an EGL setup can be used
by programs mixing these APIs, drawing (for example) a 2D vector-based user
interface from OpenVG over the top of a 3D scene from OpenGL (ES or not).

.. _EGL: https://www.khronos.org/egl
.. _`Khronos Group`: https://www.khronos.org/
