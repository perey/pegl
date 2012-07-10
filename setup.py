from distutils.core import setup

setup(
    name='Pegl',
    version='0.1a3~1.4',
    author='Tim Pederick',
    author_email='pederick@gmail.com',
    packages=['pegl', 'pegl.attribs',
              'pegl.ext', 'pegl.ext.angle', 'pegl.ext.img', 'pegl.ext.khr',
              'pegl.ext.mesa', 'pegl.ext.nok', 'pegl.ext.nv', 'pegl.ext.wl'],
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
