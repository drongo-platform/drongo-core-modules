#!/usr/bin/env python

from setuptools import find_packages, setup


setup(
    name='drongo-core-modules',
    version='0.0.1',
    description='A nano web-framework for python.',
    author='Sattvik Chakravarthy',
    author_email='sattvik@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    zip_safe=True
)
