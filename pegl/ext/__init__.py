#!/usr/bin/env python3

'''EGL extension support.

Unimplemented:
    1.  EGL_KHR_config_attribs
    17. EGL_NV_coverage_sample
    18. EGL_NV_depth_nonlinear
    24. EGL_HI_clientpixmap
    25. EGL_HI_colorformats
    30. EGL_NV_coverage_sample_resolve
    46. EGL_NV_3dvision_surface
    61. EGL_KHR_get_all_proc_addresses and
        EGL_KHR_client_get_all_proc_addresses

'''

# Copyright © 2012-13 Tim Pederick.
#
# This file is part of Pegl.
#
# Pegl is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pegl is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pegl. If not, see <http://www.gnu.org/licenses/>.

__all__ = (# Registered cross-vendor (EXT) extensions.
           'ext_bufferage', 'ext_dma_buf', 'ext_extensiontypes',
           'ext_multiview', 'ext_platform', 'ext_platform_x11',
           'ext_robustness', 'ext_swapdamage',
           # Registered vendor extensions.
           'android_blobcache', 'android_bufferimage', 'android_framebuffer',
           'android_nativesync', 'android_recordable',
           'angle_d3dtexture', 'angle_surfacepointer',
           'arm_discardmulti',
           'img_contextpriority',
           'khr_clevent', 'khr_clevent2', 'khr_context', 'khr_fifostream',
           'khr_glcolor', 'khr_glimage', 'khr_glstream', 'khr_image',
           'khr_locksurface', 'khr_locksurface3', 'khr_stream',
           'khr_streamcrossprocess', 'khr_streamsurface', 'khr_surfaceless',
           'khr_sync', 'khr_vgimage', 'khr_waitsync',
           'mesa_drmimage', 'mesa_platform_gbm',
           'nok_swapregion2',
           'nv_nativequery', 'nv_postconvert', 'nv_postsubbuffer',
           'nv_streamsync', 'nv_sync', 'nv_systime',
           # Unregistered extensions.
           'nok_swapregion', 'wl_binddisplay',
           # Stuff defined here.
           'extensions', 'load_ext')

# Standard library imports.
from ctypes import CFUNCTYPE

# Local imports.
from .. import native

# Mapping of name strings to module names.
# TODO: Separate lists for client and display extensions?
extensions = {
# Extensions in the cross-vendor (EXT) namespace.
    'EGL_EXT_create_context_robustness': 'ext_robustness',               #37
    'EGL_EXT_multiview_window': 'ext_multiview',                         #42
    'EGL_EXT_buffer_age': 'ext_bufferage',                               #52
    'EGL_EXT_image_dma_buf_import': 'ext_dma_buf',                       #53
    'EGL_EXT_swap_buffers_with_damage': 'ext_swapdamage',                #55
    'EGL_EXT_platform_base': 'ext_platform',                             #57
    'EGL_EXT_client_extensions': 'ext_extensiontypes',                   #58
    'EGL_EXT_platform_x11': 'ext_platform_x11',                          #59
    'EGL_EXT_platform_wayland': 'ext_platform_wayland',                  #63
# Extensions from the Android operating system.
    'EGL_ANDROID_framebuffer_target': 'android_framebuffer',             #47
    'EGL_ANDROID_blob_cache': 'android_blobcache',                       #48
    'EGL_ANDROID_image_native_buffer': 'android_bufferimage',            #49
    'EGL_ANDROID_native_fence_sync': 'android_nativesync',               #50
    'EGL_ANDROID_recordable': 'android_recordable',                      #51
# Extensions from ANGLE, the Almost Native Graphics Layer Engine.
    'EGL_ANGLE_query_surface_pointer': 'angle_surfacepointer',           #28
    'EGL_ANGLE_surface_d3d_texture_2d_share_handle': 'angle_d3dtexture', #29
    'EGL_ANGLE_d3d_share_handle_client_buffer': 'angle_d3dtexture',      #38
# Extensions from ARM Holdings (ARM).
    'EGL_ARM_pixmap_multisample_discard': 'arm_discardmulti',            #54
# Extensions from Imagination Technologies (IMG).
    'EGL_IMG_context_priority': 'img_contextpriority',                   #10
# Extensions from Khronos Group (KHR).
    'EGL_KHR_lock_surface': 'khr_locksurface',                            #2
    'EGL_KHR_image': 'khr_image',                                         #3
    'EGL_KHR_vg_parent_image': 'khr_vgimage',                             #4
    'EGL_KHR_gl_texture_2D_image': 'khr_glimage',                         #5
    'EGL_KHR_gl_texture_cubemap_image': 'khr_glimage',                    #5
    'EGL_KHR_gl_texture_3D_image': 'khr_glimage',                         #5
    'EGL_KHR_gl_renderbuffer_image': 'khr_glimage',                       #5
    'EGL_KHR_reusable_sync': 'khr_sync',                                  #6
    'EGL_KHR_image_base': 'khr_image',                                    #8
    'EGL_KHR_image_pixmap': 'khr_image',                                  #9
    'EGL_KHR_lock_surface2': 'khr_locksurface',                          #16
    'EGL_KHR_fence_sync': 'khr_sync',                                    #20
    'EGL_KHR_stream': 'khr_stream',                                      #32
    'EGL_KHR_stream_consumer_gltexture': 'khr_glstream',                 #33
    'EGL_KHR_stream_producer_eglsurface': 'khr_streamsurface',           #34
    'EGL_KHR_stream_producer_aldatalocator': 'khr_streammaxal',          #35
    'EGL_KHR_stream_fifo': 'khr_fifostream',                             #36
    'EGL_KHR_create_context': 'khr_context',                             #39
    # This extension requires absolutely no new code on the EGL side, but a
    # module for it is provided anyway.
    'EGL_KHR_surfaceless_context': 'khr_surfaceless',                    #40
    'EGL_KHR_stream_cross_process_fd': 'khr_streamcrossprocess',         #41
    'EGL_KHR_wait_sync': 'khr_waitsync',                                 #43
    'EGL_KHR_cl_event': 'khr_clevent',                                   #60
    'EGL_KHR_lock_surface3': 'khr_locksurface3',                         #64
    'EGL_KHR_cl_event2': 'khr_clevent2',                                 #65
    'EGL_KHR_gl_colorspace': 'khr_glcolor',                              #66
# Extensions from the Mesa 3D library.
    'EGL_MESA_drm_image': 'mesa_drmimage',                               #26
    'EGL_MESA_platform_gbm': 'mesa_platform_gbm',                        #62
# Extensions from Nokia (NOK).
    'EGL_NOK_swap_region': 'nok_swapregion',                    # Unofficial
    'EGL_NOK_swap_region2': 'nok_swapregion2',                           #23
# Extensions from NVIDIA Corporation (NV).
    'EGL_NV_sync': 'nv_sync',                                            #19
    'EGL_NV_post_sub_buffer': 'nv_postsubbuffer',                        #27
    'EGL_NV_system_time': 'nv_systime',                                  #31
    # This extension requires absolutely no new code on the EGL side, but a
    # module for it is provided anyway.
    'EGL_NV_post_convert_rounding': 'nv_postconvert',                    #44
    'EGL_NV_native_query': 'nv_nativequery',                             #45
    'EGL_NV_stream_sync': 'nv_streamsync',                               #56
# Extensions from the Wayland compositor (WL).
    'EGL_WL_bind_wayland_display': 'wl_binddisplay'             # Unofficial
    }

def load_ext(fname, return_type, arg_types, check_errors=True, **kwargs):
    '''Load an extension function at runtime.

    Keyword arguments:
        fname -- The name of the extension function, given as a byte
            string.
        return_type -- The ctypes type that the extension function
            returns.
        arg_types -- A sequence listing the ctypes types of the
            arguments to the extension function.
        check_errors -- Whether to wrap the loaded function with EGL
            error checking. The default is True.
        Further keyword arguments are passed to the error_check function
        if check_errors was True; otherwise they are ignored.

    '''
    void_func = native.eglGetProcAddress(fname)
    if void_func is None:
        # Extension not available.
        raise ImportError("extension function '{}' not "
                          "available".format(fname.decode()))
    # Cast the pointer to a function pointer with the correct types.
    typed_func = CFUNCTYPE(return_type, *arg_types)(void_func)
    if check_errors:
        return native.error_check(typed_func, **kwargs)
    else:
        return typed_func
