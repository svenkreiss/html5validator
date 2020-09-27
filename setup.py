from setuptools import setup

import sys

from html5validator import __version__

INSTALL_REQUIRES = [
    "PyYAML"
]


# add argparse dependency for python < 2.7
major, minor1, minor2, release, serial = sys.version_info
if major <= 2 and minor1 < 7:
    INSTALL_REQUIRES.append('argparse==1.2.1')


setup(
    name='html5validator',
    version=__version__,
    packages=['html5validator', 'html5validator.tests', 'vnujar'],
    license='MIT',
    description='Validate HTML5 files.',
    long_description=open('README.rst').read(),
    author='Sven Kreiss',
    author_email='me@svenkreiss.com',
    url='https://github.com/svenkreiss/html5validator',

    include_package_data=True,
    zip_safe=False,
    python_reqires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'tests': [
            'hacking',
            'nose',
        ],
    },
    entry_points={
        'console_scripts': [
            'html5validator = html5validator.cli:main',
        ]
    },

    tests_require=['nose'],
    test_suite='nose.collector',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
