from distutils.core import setup

setup(
    name='ogrtools',
    version='0.7.2',
    author='Pirmin Kalberer',
    author_email='pka@sourcepole.ch',
    packages=['ogrtools', 'ogrtools.test'],
    scripts=['bin/ogr'],
    url='http://pypi.python.org/pypi/ogrools/',
    license='LICENSE.txt',
    description='Collection of libraries and tools built with the Python API of OGR.',
    long_description=open('README.rst').read(),
)
