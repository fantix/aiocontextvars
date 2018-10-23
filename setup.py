#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'contextvars==2.3;python_version<"3.7"',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
    'pytest-asyncio==0.8.0',
]

setup(
    name='aiocontextvars',
    version='0.2.0',
    description="Asyncio support for PEP-567 contextvars backport.",
    long_description=readme + '\n\n' + history,
    author="Fantix King",
    author_email='fantix.king@gmail.com',
    url='https://github.com/fantix/aiocontextvars',
    packages=find_packages(include=['aiocontextvars']),
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.5',
    license="BSD license",
    zip_safe=False,
    keywords='aiocontextvars',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
