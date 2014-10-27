from setuptools import setup

import re
import sys

# workaround: nosetests don't exit cleanly with older
# python version (<=2.6 and even <2.7.4)
try:
    import multiprocessing
except ImportError:
    pass


INSTALL_REQUIRES = []


# extract html5validator version from __init__.py
with open('html5validator/__init__.py', 'r') as f:
    INIT = f.read()
    VERSION = next(re.finditer('__version__ = \"(.*?)\"', INIT)).group(1)


# add argparse dependency for python < 2.7
major, minor1, minor2, release, serial = sys.version_info
if major <= 2 and minor1 < 7:
    INSTALL_REQUIRES.append('argparse==1.2.1')


setup(
    name='html5validator',
    version=VERSION,
    packages=['html5validator', 'vnujar'],
    license='MIT',
    description='Validate HTML5 files.',
    long_description=open('README.rst').read(),
    author='Sven Kreiss',
    author_email='me@svenkreiss.com',
    url='https://github.com/svenkreiss/html5validator',

    include_package_data=True,

    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'html5validator = html5validator.cli:main',
        ]
    },

    tests_require=[
        'nose',
    ],
    test_suite='nose.collector',

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ]
)
