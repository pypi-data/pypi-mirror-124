#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
    author="Walken Talk",
    author_email='walkentalk@pm.me',
    python_requires='>=3.6',
    description="Blah.",
    license="MIT license",
    include_package_data=True,
    keywords='etherscanwrapper',
    name='etherscanwrapper',
    packages=find_packages(include=['etherscanwrapper', 'etherscanwrapper.*']),
    url='https://github.com/walkentalk/etherscanwrapper',
    version='0.1.0',
    zip_safe=False,
)
