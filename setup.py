from distutils.core import setup

setup(
    name='ogrtools',
    version='0.7.3',
    author='Pirmin Kalberer',
    author_email='pka@sourcepole.ch',
    packages=['ogrtools', 'ogrtools.interlis',
              'ogrtools.ogrtransform', 'ogrtools.pyogr',
              'ogr_cli'],
    url='https://github.com/sourcepole/ogrtools',
    download_url='https://github.com/sourcepole/mypackage/tarball/0.7.3',
    license='LICENSE.txt',
    description='Collection of libraries and tools built with the Python API of OGR.',
    long_description=open('README.rst').read(),
    #requires_external = 'GDAL (>=1.11.0)',
    # tests_require=['nose'],
    # test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    entry_points={
        'console_scripts': ['ogr = ogr_cli.ogr:main'],
    }
    )
