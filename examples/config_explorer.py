#!/usr/bin/env python3

"""Config Explorer: Show EGL config information in a GUI

This is a Pegl demonstration application that loads the default EGL
display, gets a list of all the configurations it supports, and shows
information about those configurations in a Tkinter GUI.

The displayed information comprises:

* The index of the configuration in the list provided by the EGL
  implementation.
* The implementation's internal ID for the configuration.
* Which rendering APIs are supported (from OpenGL ES versions 1, 2, and
  3, OpenGL, OpenVG, and platform-defined native rendering APIs). A
  check mark means the API is supported, while an asterisk means that
  the configuration may not meet the API's conformance requirements.
* The number of bits in the color buffer.
* The type of color buffer, either 'RGB' or 'L' (luminance).
* The allocation of bits in the color buffer to each component.
* The number of bits in the alpha mask, depth, and stencil buffers.
* Whether a multisample buffer is present, and if so, how many samples
  are generated per pixel, and whether multisampling can be resolved by
  a box filter.
* Which surface types are supported, out of the three defined by EGL:
  pbuffer, pixmap, and window surfaces.
* Which OpenVG rendering options are enabled.
* The maximum size of a pbuffer surface, given as width × height, plus
  the maximum number of pixels if this is less than width × height.
* The framebuffer overlay or underlay level.
* The range of frames allowed between swaps, and whether the color buffer
  is preserved after swaps.
* Which texture types (out of RGB and RGBA) may be bound.
* Which color (if any) is defined as transparent.
* Any caveats that apply to the configuration.
* The native visual that will be associated with window surfaces.

Note that some of the requested attributes are not available prior to
EGL 1.3, so this application will not run on earlier versions.

"""

# Copyright © 2022 Tim Pederick.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import tkinter
from tkinter import ttk

import pegl

# Functions to generate user-friendly representations of config values.

def bind_to_texture(cfg):
    """Describe a config's allowed texture bindings."""
    strings = []

    if cfg.bind_to_texture_rgb:
        strings.append('RGB')
    if cfg.bind_to_texture_rgba:
        strings.append('RGBA')

    return ', '.join(strings)


def color_bits(cfg):
    """Describe a config's color bit allocations."""
    r, g, b = cfg.red_size, cfg.green_size, cfg.blue_size
    l = cfg.luminance_size
    a = cfg.alpha_size
    amask = cfg.alpha_mask_size

    strings = []
    if (r, g, b) > (0, 0, 0):
        if l > 0:
            # That shouldn't happen...
            strings.append(f'{r}/{g}/{b} RGB')
            strings.append(f'{l} luminance')
            if a > 0:
                strings.append(f'{a} alpha')
        elif a > 0:
            strings.append(f'{r}/{g}/{b}/{a} RGBA')
        else:
            strings.append(f'{r}/{g}/{b} RGB')
    elif l > 0:
        if a > 0:
            strings.append(f'{l}/{a} LA')
        else:
            strings.append(f'{l} luminance')

    return ', '.join(strings)


friendly_buffer_types = {pegl.ColorBufferType.RGB: 'RGB',
                         pegl.ColorBufferType.LUMINANCE: 'L'}

friendly_caveats = {pegl.ConfigCaveat.NON_CONFORMANT: 'Non-conformant',
                    pegl.ConfigCaveat.SLOW: 'Slow'}


def friendly_enum(enumattr, namedict, default=''):
    """Make a lookup function for user-friendly enumeration names."""
    return lambda cfg: namedict.get(getattr(cfg, enumattr), default)


def hexcode(components):
    """Get the hexadecimal color code for a given color."""
    return ''.join('#', *(format(component, '0>2x')
                          for component in components))


def is_supported(api_flag):
    """Make a function to check a configuration for API support."""
    # The case where support is not claimed, but conformance is, is ignored.
    return lambda cfg: ('✓' + ('*' if api_flag not in cfg.conformant else '')
                        if api_flag in cfg.renderable_type else '')


def is_native_supported(cfg):
    """Check a configuration for native API support."""
    return '✓' if cfg.native_renderable else ''


def max_pbuffer(cfg):
    """Describe the maximum pbuffer size that a config allows."""
    w, h = cfg.max_pbuffer_width, cfg.max_pbuffer_height
    px = cfg.max_pbuffer_pixels
    calc_px = w * h

    strings = [f'{cfg.max_pbuffer_width}×{cfg.max_pbuffer_height}']
    if px < calc_px:
        strings.append(f'({px} px)')

    return ' '.join(strings)


def multisampling(cfg):
    """Describe the multisample support of a config."""
    strings = []
    
    if cfg.sample_buffers == 0:
        strings.append('No')
    elif cfg.sample_buffers == 1:
        if cfg.samples > 0:
            strings.append(f'×{cfg.samples}')
        else:
            # Shouldn't happen.
            strings.append('?')
    else:
        # Shouldn't happen.
        strings.append(f'{cfg.sample_buffers} buffers')
        if cfg.samples > 0:
            strings.append(f'×{cfg.samples}')

    if pegl.SurfaceTypeFlag.MULTISAMPLE_RESOLVE_BOX in cfg.surface_type:
        strings.append('box filter')
    
    return ', '.join(strings)


def native_visual(cfg):
    """Describe the native visual associated with a config."""
    strings = []

    if cfg.native_visual_type is not None:
        strings.append(f'Type {cfg.native_visual_type}')
    if cfg.native_visual_id != 0:
        strings.append(f'ID {cfg.native_visual_id}')

    return ', '.join(strings)

def surface_type(cfg):
    """List the surface types supported by a config."""
    strings = []

    if pegl.SurfaceTypeFlag.PBUFFER in cfg.surface_type:
        strings.append('pbuffer')
    if pegl.SurfaceTypeFlag.PIXMAP in cfg.surface_type:
        strings.append('pixmap')
    if pegl.SurfaceTypeFlag.WINDOW in cfg.surface_type:
        strings.append('window')

    return ', '.join(strings)
    

def swap_interval(cfg):
    """Describe the range of swap intervals that a config allows."""
    strings = [f'{cfg.min_swap_interval}–{cfg.max_swap_interval}']
    if pegl.SurfaceTypeFlag.SWAP_BEHAVIOR_PRESERVED in cfg.surface_type:
        strings.append('(preserved)')

    return ' '.join(strings)


def transparent_type(cfg):
    """Describe a config's transparency type."""
    if cfg.transparent_type == pegl.TransparentType.RGB:
        return hexcode(cfg.transparent_red_value, cfg.transparent_green_value,
                       cfg.transparent_blue_value)
    elif cfg.transparent_type is None:
        return 'N/A'
    else:
        return '?'


def vg_support(cfg):
    """Describe OpenVG-specific rendering support."""
    strings = []

    if pegl.SurfaceTypeFlag.VG_ALPHA_FORMAT_PRE in cfg.surface_type:
        strings.append('premultiplied alpha')
    if pegl.SurfaceTypeFlag.VG_COLORSPACE_LINEAR in cfg.surface_type:
        strings.append('linear colorspace')

    return ', '.join(strings)


# Definitions of columns to display in the table.

NARROW, REGULAR, WIDE, HUGE = 30, 40, 50, 110

columns = {'config_num': (tkinter.E, NARROW, '#', None), 
           'config_id': (tkinter.E, NARROW, 'ID', lambda cfg: cfg.config_id),
           'support_es1': (tkinter.CENTER, NARROW, 'ES1',
                           is_supported(pegl.ClientAPIFlag.OPENGL_ES)),
           'support_es2': (tkinter.CENTER, NARROW, 'ES2',
                           is_supported(pegl.ClientAPIFlag.OPENGL_ES2)),
           'support_es3': (tkinter.CENTER, NARROW, 'ES3',
                           is_supported(pegl.ClientAPIFlag.OPENGL_ES3)),
           'support_gl': (tkinter.CENTER, NARROW, 'GL',
                          is_supported(pegl.ClientAPIFlag.OPENGL)),
           'support_vg': (tkinter.CENTER, NARROW, 'VG',
                          is_supported(pegl.ClientAPIFlag.OPENVG)),
           'support_native': (tkinter.CENTER, NARROW, 'Native',
                              is_native_supported),
           'color_buffer_size': (tkinter.E, REGULAR, 'Color',
                                 lambda cfg: cfg.buffer_size),
           'color_buffer_type': (tkinter.W, REGULAR, 'Type',
                                 friendly_enum('color_buffer_type',
                                               friendly_buffer_types,
                                               default='?')),
           'color_buffer_bits': (tkinter.W, HUGE, 'Bit allocations',
                                 color_bits),
           'alpha_mask_size': (tkinter.E, REGULAR, 'Mask',
                               lambda cfg: cfg.alpha_mask_size),
           'depth_size': (tkinter.E, REGULAR, 'Depth',
                          lambda cfg: cfg.depth_size),
           'stencil_size': (tkinter.E, REGULAR, 'Stencil',
                            lambda cfg: cfg.stencil_size),
           'multisampling': (tkinter.W, REGULAR, 'Multisampling',
                             multisampling),
           'surface_type': (tkinter.W, HUGE, 'Surface types',
                            surface_type),
           'vg_rendering': (tkinter.W, WIDE, 'VG options',
                            vg_support),
           'max_pbuffer': (tkinter.W, HUGE, 'Max pbuffer size',
                           max_pbuffer),
           'level': (tkinter.E, REGULAR, 'Level',
                     lambda cfg: cfg.level),
           'swap_interval': (tkinter.W, HUGE, 'Swap interval',
                             swap_interval),
           'bind_to_texture': (tkinter.W, REGULAR, 'Bind',
                               bind_to_texture),
           'transparent': (tkinter.W, WIDE, 'Transparency',
                           transparent_type),
           'config_caveat': (tkinter.W, WIDE, 'Caveat',
                             friendly_enum('config_caveat',
                                           friendly_caveats)),
           'native_visual': (tkinter.W, HUGE, 'Native visual', native_visual)}


# GUI functions.

def prepare_table(parent, columns, yscroll=None):
    """Set up headings and columns for a GUI table.

    The table is created as a Treeview widget with the tree column
    hidden.

    """
    table = ttk.Treeview(parent,
                         yscrollcommand=(None if yscroll is None else
                                         yscroll.set))
    table['columns'] = tuple(columns.keys())

    # Hide the tree column.
    table.column('#0', width=0, stretch=tkinter.NO)
    table.heading('#0', text='')

    for key, (anchor, width, text, _) in columns.items():
        table.column(key, anchor=anchor, width=width)
        table.heading(key, text=text)

    return table


class ConfigExplorer(tkinter.Tk):
    def __init__(self):
        """Create the Config Explorer GUI."""
        super().__init__()

        # Get the EGL information.
        dpy = pegl.Display()
        version_info = 'EGL version: ' + dpy.version_string
        vendor_info = 'Vendor: ' + dpy.vendor
        all_configs = dpy.get_configs()

        # Prepare the GUI.
        self.title('EGL Config Explorer')

        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both')

        label_frame = ttk.Frame(main_frame)
        label_frame.pack(fill='x')

        version_label = ttk.Label(label_frame, text=version_info)
        version_label.pack(side='top', fill='x')
        vendor_label = ttk.Label(label_frame, text=vendor_info)
        vendor_label.pack(side='bottom', fill='x')

        table_frame = ttk.Frame(main_frame)
        table_frame.pack(side='bottom', expand=True, fill='both')

        table_scroll = ttk.Scrollbar(table_frame)
        table_scroll.pack(side='right', fill='y')

        table = prepare_table(table_frame, columns, table_scroll)
        table_scroll.config(command=table.yview)

        # Populate the table.
        for n, cfg in enumerate(all_configs):
            friendly_values = tuple((n if fn is None else fn(cfg))
                                    for (*_, fn) in columns.values())
            table.insert(parent='', index='end', iid=n, text='',
                         values=friendly_values)
        table.pack(side='left', expand=True, fill='both')

        # Terminate the EGL setup.
        del dpy


if __name__ == '__main__':
    app = ConfigExplorer()
    app.mainloop()
