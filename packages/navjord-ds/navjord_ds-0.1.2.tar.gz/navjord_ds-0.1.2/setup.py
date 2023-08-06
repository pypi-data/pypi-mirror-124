#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

readme = ""
history = ""

requirements = [ ]

test_requirements = [ ]

setup(
    author="Jørgen Navjord",
    author_email='navjordj@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description=".",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='navjord_ds',
    name='navjord_ds',
    packages=find_packages(include=['navjord_ds', 'navjord_ds.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/navjordj/navjord_ds',
    version='0.1.2',
    zip_safe=False,
)
