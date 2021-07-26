#!/usr/bin/env python3

from setuptools import find_packages, setup

INSTALL_REQUIRES = ['pandas >= 0.18.0', 'pathlib']
TESTS_REQUIRE = ['pytest >= 2.7.1']

setup(
    name='tools_bauerlab',
    version='0.1',
    license='MIT',
    description=('Tools to read and process data from the lab of Sebastian Bauer (University of Frankfurt)'),
    author='Tristan Stoeber',
    author_email='tristan.stoeber@posteo.net',
    url='https://github.com/trieschlab/tools_bauerlab',
    packages=find_packages(),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
)
