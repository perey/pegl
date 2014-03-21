# Setup file for Pegl.
#
# Copyright © 2012-14 Tim Pederick.
# 
# Some parts based on the PyPA sample project:
#   https://github.com/pypa/sampleproject/
# Copyright © 2013-14 The Python Packaging Authority.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Standard library imports.
import os.path
import re
from distutils.core import setup

version_re = re.compile('''^\s*__version__ = ['"]([^'"]+)['"]''')

def get_version(package, filename='__init__.py'):
    '''Find the __version__ attribute of the specified package.'''
    with open(os.path.join(package, filename)) as f:
        for line in f:
            match = version_re.search(line)
            if match:
                return match.group(1)
    raise RuntimeError('no version information found')

setup(
    name='Pegl',
    version=get_version('pegl'),
    author='Tim Pederick',
    author_email='pederick@gmail.com',
    packages=['pegl', 'pegl.attribs', 'pegl.ext'],
    url='https://github.com/perey/pegl',
    description='Python 3 wrapper for the EGL API',
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License v3 '
                 'or later (GPLv3+)',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Topic :: Multimedia :: Graphics',
                 'Topic :: Software Development :: Libraries'],
    long_description=open('README.rst', 'rt').read(),
)
