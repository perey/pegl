#!/usr/bin/env python3

'''EGL configuration management.'''

# Standard library imports.
from ctypes import POINTER, c_int, c_void_p

# Local imports.
from . import egl, error_check

MAX_CONFIGS = 256 # Arbitrary!
int_p = POINTER(c_int)

def get_configs(display, attribs=None):
    '''Get supported configurations for a given display.'''
    configs = (c_void_p * MAX_CONFIGS)()
    actual_count = int_p()
    actual_count.contents = c_int(0)

    if attribs is None:
        error_check(egl.eglGetConfigs(display, configs, MAX_CONFIGS,
                                      actual_count))
    else:
        error_check(egl.eglChooseConfig(display, attribs, configs, MAX_CONFIGS,
                                        actual_count))

    return tuple(Config(cfg, display) for cfg in configs[:actual_count[0]])

class Config:
    '''A set of EGL configuration options.'''
    def __init__(self, chandle, display):
        '''Initialise the configuration.'''
        self.chandle = chandle
        self.display = display

    def _attr(self, attr):
        '''Get the value of a configuration attribute.'''
        result = int_p()

        errorcheck(egl.eglGetConfigAttrib(self.display, self, attr, result))
        return result[0]
