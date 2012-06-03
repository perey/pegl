#!/usr/bin/env python3

'''EGL 1.4 attribute lists.'''

def dont_care_or(expected_type):
    '''Create a type for when a don't-care value is permissible.'''
    DONT_CARE = -1

    class WrappedType:
        '''Wrap a C type so that its value can be DONT_CARE.'''
        def __init__(self, val):
            self.value = val
        def __setattr__(self, attr, val):
            if attr == 'value' and value is not DONT_CARE:
                val = expected_type(val)
            super().__setattr__(attr, val)
        def __repr__(self):
            if self.value is DONT_CARE:
                return 'DONT_CARE'
            else:
                return repr(self.value)
        @property
        def _as_parameter_(self):
            if self.value is DONT_CARE:
                return DONT_CARE
            try:
                return self.value._as_parameter_
            except AttributeError:
                return self.value

    return WrappedType
