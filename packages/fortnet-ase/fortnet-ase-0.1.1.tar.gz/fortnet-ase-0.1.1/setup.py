#!/usr/bin/env python3
from distutils.core import setup


setup(
    name='fortnet-ase',
    version='0.1.1',
    description='Interfacing Fortnet with the Atomic Simulation Environment',
    author='T. W. van der Heide',
    url='https://github.com/vanderhe/fortnet-ase',
    platforms='platform independent',
    package_dir={'': 'src'},
    packages=['fnetase'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    long_description='''
Interfacing Fortnet with the Atomic Simulation Environment
----------------------------------------------------------
fortnet-ase provides an interface between the neural network
implementation Fortnet and the Atomic Simulation Environment.
''',
    requires=['pytest', 'numpy', 'h5py', 'ase']
)
