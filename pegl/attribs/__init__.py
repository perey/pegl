#!/usr/bin/env python3

'''EGL attribute lists.'''

# Copyright © 2012 Tim Pederick.
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

__all__ = ('NONE', 'NO_TEXTURE', 'UNKNOWN_VALUE', 'SCALE_FACTOR',
           'Attribs', 'AttribList', 'BitMask', 'Details',
           'attr_convert', 'scaled',
           'config', 'context', 'surface')

# Standard library imports.
from collections import namedtuple
from ctypes import c_int, POINTER
from itertools import compress

# ctypes doesn't allow passing an array of ints where we've told it to expect
# a pointer to int, so we have to cast the former to the latter.
int_p = POINTER(c_int)

# Symbolic constants used here and/or in more than one module in this package.
NONE = 0x3038
NO_TEXTURE = 0x305C
UNKNOWN_VALUE = -1
SCALE_FACTOR = 10000 # Used to store floats as ints by scaling them up.

# A symbolic don't-care value that can't be confused with anything else. This
# is only used when asking EGL for configurations that match requirements, but
# since AttribList needs to know when to accept DONT_CARE, we define it here.
class DONT_CARE:
    '''A don't-care value for an attribute.'''
    _as_parameter_ = -1

# Named tuple for storing the details of an attribute field. Note that the
# "default" field may only contain the default for setting an attribute (or
# the default requested when looking for configs), not the default for an
# unset value -- the implementation might define those itself.
Details = namedtuple('Details', ('desc', 'values', 'default'))

# Bit mask attribute types.
class BitMask:
    '''A bit mask with convenient Python representations.

    Class attributes:
        bit_names -- A sequence of names for the bits in the mask
            (least significant first). Any bits without names have
            None for the name. Each bit with a name in bit_names
            can also be accessed as an instance attribute with that
            name (assuming the name is a valid Python identifier).

    Instance attributes:
        bits -- The raw bits of the mask (least significant first).

    '''
    bit_names = []
    extensions = []

    @classmethod
    def _make_property(cls, bit_number):
        '''Create a property to get and set a specified bit value.

        This is necessary because code like this doesn't work:
        >>> getter = lambda self: self.bits[bit_number]

        For some reason, probably to do with the scope of the variable
        bit_number, every function so defined ends up taking on the same
        value of bit_number (the value it last had).

        '''
        def getter(self):
            '''Get the value of the bit at position {}.'''.format(bit_number)
            return self.bits[bit_number]

        def setter(self, val):
            '''Set or unset the bit at position {}.'''.format(bit_number)
            self.bits[bit_number] = bool(val)

        return property(getter, setter)

    @classmethod
    def extend(cls, bit_number, bit_name, override=False):
        '''Extend the bit mask by assigning a new bit name.

        Keyword arguments:
            bit_number -- The bit number to assign the new name to,
                counting from 0 (the least significant bit).
            bit_name -- The name to assign to the new bit.
            override -- Whether or not the new name can replace an
                existing name (either a standard name or from an
                extension). If False (the default), only bits with names
                that are currently None, or bits that enlarge the bit
                mask, may be given new names.

        '''
        off_end = bit_number - len(cls.bit_names)
        if off_end < 0:
            # The bit number falls within the current bit mask length.
            if (override or cls.bit_names[bit_number] is None):
                # Okay to assign new name.
                cls.bit_names[bit_number] = bit_name
            else:
                raise TypeError('could not rename existing bit (use override '
                                'argument to force change)')
        else:
            # The bit number is off the end of the bit mask.
            cls.bit_names.extend([None] * off_end + [bit_name])
        cls.extensions.append(bit_name)

    def __init__(self, *args, **kwargs):
        '''Set up the bit mask.

        Positional arguments:
            Integer values to use in initialising the bit mask. Each
            value is used in turn, effectively being OR'd together
            to create the mask.

        Keyword arguments:
            Initial bit values by name. The boolean value of the
            argument sets the relevant bit, overriding anything set
            from positional arguments.

        '''
        self.bits = [False] * len(self.bit_names)

        # Set up access to bits by name.
        bit_number = -1
        for posname in self.bit_names:
            bit_number += 1
            if posname is None:
                # Unnamed bit.
                continue
            setattr(self.__class__, posname, self._make_property(bit_number))

        # Initialise values from positional arguments.
        for mask in args:
            self._from_int(mask)

        # Initialise values from keyword arguments.
        for bit_name in kwargs:
            # If the keyword is not a valid bit name, we allow the
            # resulting AttributeError to propagate upwards.
            setter = getattr(self.__class__, bit_name).fset
            setter(self, kwargs[bit_name])

    @property
    def _as_parameter_(self):
        '''Get the bit mask value for use by foreign functions.'''
        return int(self)

    @property
    def _flags_set(self):
        '''Get the set bits by name.'''
        return tuple(compress(self.bit_names, self.bits))

    def __int__(self):
        '''Convert the bits to the corresponding integer.'''
        return sum(2 ** i if bit else 0 for i, bit in enumerate(self.bits))

    def __str__(self):
        '''List the set bits by name, separated by commas.'''
        return ','.join(self._flags_set)

    def _from_int(self, mask):
        '''Set this bit mask from an integer mask value.

        Keyword arguments:
            mask -- The integer mask to use. Any bits in excess of
                this mask's width are ignored.

        '''
        pos = 0
        mask = int(mask)
        # Go bit by bit until we run out of bits in either mask.
        while mask > 0 and pos < len(self.bits):
            mask, bit = divmod(mask, 2)
            self.bits[pos] = bool(bit)
            pos += 1


class Attribs:
    '''A set of EGL attributes.

    Subclasses of this class define attributes for different EGL objects
    such as configurations and surfaces. All useful information is
    available in class attributes and class methods, so these classes do
    not need to be instantiated.

    Class attributes:
        details -- A mapping with the attribute's integer value as the
            key, and a Details named-tuple instance (with a text
            description, the attribute type, and its default value) as
            the value.
        extensions -- A mapping of extension attributes loaded on this
            class to their integer values. By default, this is empty.
        Additionally, symbolic constants for all the known attributes
        are available as class attributes. Their names are the same as
        in the EGL standard, except without the EGL_ prefix.

    '''
    extensions = {}

    @classmethod
    def desc(cls, value):
        '''Get a textual description of a given attribute.

        This may also be used to test for the validity of a given
        attribute. If the return value is None, the value supplied does
        not map to any known attribute.

        Keyword arguments:
            value -- The value representing the desired attribute.

        '''
        details = cls.details.get(value)
        return (None if details is None else details.desc)

    @classmethod
    def extend(cls, attr_name, value, attr_type, default, desc=None):
        '''Load an extension attribute into this class.

        Keyword arguments:
            attr_name -- The name of the extension attribute.
            attr_value -- The integer constant that represents the
                extension attribute.
            attr_type -- The type of the values that may be assigned to
                this attribute.
            default -- The default that this attribute takes.
            desc -- An optional string describing the attribute.

        '''
        # TODO: Track loaded extensions and filter by name string, in a similar
        # manner to the ext.khr.image.Image class. This is useful because some
        # extension modules (including that one and ext.khr.glimage) define
        # more than one extension, not all of which need be supported for the
        # module to be loaded.
        cls.extensions[attr_name] = value
        cls.details[value] = Details('An extension attribute'
                                     if desc is None else desc,
                                     attr_type, default)


class AttribList:
    '''A list of EGL attributes.

    This class implements the mapping interface, namely the __getitem__,
    __setitem__, __delitem__ and items methods.

    Instance attributes:
        _items -- Direct access to the attributes set in this list.
        attribs -- The subclass of Attribs defining the attributes
            available in this list.

    '''
    def __init__(self, attribs, mapping=None):
        '''Initialise the attribute list.

        Keyword arguments:
            attribs -- As the instance attribute.
            mapping -- An optional dictionary from which to initialise
                this attribute list.

        '''
        self.attribs = attribs
        self._items = {}

        if mapping is not None:
            for key, val in mapping.items():
                self[key] = val

    def __getitem__(self, index):
        '''Get the value of an attribute, or None if it is unset.

        See also get(), which returns the default for an attribute
        (rather than None) if it is unset.

        Keyword arguments:
            index -- The attribute requested. This is either a value
                from the attribs member of this AttribList, or a string
                giving the name of such a value.

        '''
        # If given a string, look up the index by that name.
        if type(index) is str:
            index = self._by_name(index)

        if self.attribs.desc(index) is None:
            raise ValueError('not a valid attribute type')
        return self._items.get(index)

    def __setitem__(self, index, val):
        '''Set the value of an attribute.

        Keyword arguments:
            index -- The attribute to set. This is either a value from
                the attribs member of this AttribList, or a string
                giving the name of such a value.
            val -- The value to set for the attribute. If None, the
                attribute will be set to its default value instead.

        '''
        # If given a string, look up the index by that name.
        if type(index) is str:
            index = self._by_name(index)

        # Check that the given value is valid.
        try:
            details = self.attribs.details[index]
        except KeyError:
            # The set of attributes doesn't have this one.
            raise ValueError('not a valid attribute type')

        if val is None:
            # Setting an attribute to None makes it take on its default value
            # (as defined by Pegl, not necessarily by the EGL implementation).
            # If you want to actually clear an attribute from the list, use:
            #     >>> del attr_list[i]
            val = details.default
        elif val is DONT_CARE:
            # Setting a value to DONT_CARE is only allowed for one attribute
            # set, namely ConfigAttribs. We can recognise that by the presence
            # of the must_care class attribute.
            try:
                if index in self.attribs.must_care:
                    # The set of attributes understands DONT_CARE, but doesn't
                    # allow it for this specific attribute.
                    raise ValueError('attribute cannot be DONT_CARE')
            except AttributeError:
                # This set of attributes doesn't even care about DONT_CARE.
                # This is the case for all of them except ConfigAttribs.
                raise ValueError('attribute cannot be DONT_CARE')
            # Otherwise, DONT_CARE is fine and we drop right on through.
        else:
            # Is this value legal for this attribute?
            try:
                # Are the allowed values given as an iterable object? This
                # works for enumerations (named tuple instances).
                if val not in details.values:
                    raise ValueError('not a legal attribute value')
            except TypeError:
                # "in" is not applicable to this attribute type. Try passing
                # the given value to the attribute type instead. This works for
                # BitMask, c_int, bool, and scaled.
                if not (type(val) is type(details.values) or
                        type(val) is details.values):
                    val = details.values(val)
                # Otherwise, the value is already of the type indicated by
                # details.values, so leave it untouched.

        self._items[index] = val

    def __delitem__(self, index):
        '''Remove the value set for an attribute.

        Keyword arguments:
            index -- The attribute to delete.

        '''
        # If given a string, look up the index by that name.
        if type(index) is str:
            index = self._by_name(index)

        del(self._items[index])

    def _by_name(self, attr_name):
        '''Look up an attribute index by its name.

        Keyword arguments:
            attr_name -- A string giving the name of the attribute.

        '''
        try:
            # Try loading as an extension attribute first.
            return self.attribs.extensions[attr_name]
        except KeyError:
            # Not an extension. If this fails too, we'll let the
            # AttributeError propagate upwards.
            return getattr(self.attribs, attr_name)

    @property
    def _as_parameter_(self):
        '''Convert to an array for use by foreign functions.'''
        arr_len = 2 * len(self._items) + 1
        arr_type = c_int * arr_len

        arr = []
        for key, value in self.items():
            arr.append(key)
            try:
                # Does the value have a means to convert to a ctypes parameter?
                arr.append(value._as_parameter_)
            except AttributeError:
                # No. Leave it as-is.
                arr.append(value)
        # Terminate the array with NONE.
        arr.append(NONE)

        # Turn the array-of-ints into a pointer-to-int, to keep ctypes happy.
        return int_p(arr_type(*arr))

    def get(self, index):
        '''Get the value of an attribute, or its default if it is unset.

        See also __getitem__(), which returns None if it is unset.

        Keyword arguments:
            index -- The attribute requested. This is either a value
                from the attribs member of this AttribList, or a string
                giving the name of such a value.

        '''
        # Look up the value by the conventional method.
        val = self[index]
        if val is None:
            # Not set; use the default.
            return self.attribs.details[value].default
        else:
            return val

    def items(self):
        '''Iterate over key-value pairs of attributes.'''
        return self._items.items()


def attr_convert(attr, value, attribs):
    '''Convert a retrieved attribute value to something meaningful.

    Keyword arguments:
        attr -- The identifier of the attribute in question.
        value -- The raw value retrieved for the attribute.
        attribs -- The Attribs subclass to which this attribute belongs.

    '''
    details = attribs.details[attr]
    if details.values is bool:
        return bool(value)
    elif value == details.default == UNKNOWN_VALUE:
        # We recognise an attribute that allows UNKNOWN_VALUE by seeing whether
        # that is its default. If so, and that's what the value is...
        return None
    elif details.values is scaled:
        # It's a scaled value, so undo the scaling.
        return scaled(value, scale_down=True)
    elif any((value == none_val and isinstance(details.values, tuple) and
             none_val in details.values) for none_val in (NONE, NO_TEXTURE)):
        # The value is an EGL symbolic constant analogous to None, in an
        # enumeration (named tuple) that supports it.
        return None
    else:
        try:
            if issubclass(details.values, BitMask):
                return details.values(value)
        except TypeError:
            # details.values is not a class, let alone a subclass of BitMask.
            pass

    # Finally...
    return value

def scaled(num, scale_down=False):
    '''Convert between a floating point value and an integer.

    Conversion is achieved by multiplying the floating point value by a
    fixed scale factor (set at 10000 by the EGL standard) and then
    truncating the result.

    Keyword arguments:
        num -- The number to be rescaled.
        scale_down -- If True, perform the reverse operation (i.e. from
            int to float). The default is False (i.e. float to int).

    '''
    num = float(num)
    if scale_down:
        return num / SCALE_FACTOR
    else:
        return int(num * SCALE_FACTOR)
