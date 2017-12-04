""" Setup script for graphene-mongoengine """

import sys
import ast
import re

from setuptools import find_packages, setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('graphene_mongoengine/__init__.py', 'rb') as f:
    match = _version_re.search(f.read().decode('utf-8')).group(1)
    version = str(ast.literal_eval(match))


setup(
    name='graphene-mongoengine',
    version=version,

    description='Graphene MongoEngine integration',
    long_description=open('README.md').read(),

    url='https://github.com/ramarivera/graphene-mongoengine',

    author='Ramiro Rivera',
    author_email='ramarivera@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    keywords='api graphql protocol rest relay graphene mongoengine',

    packages=find_packages(exclude=['tests']),

    install_requires=[
        'graphene>=2.0',
        'mongoengine',
        'singledispatch>=3.4.0.3',
        'iso8601'
    ],
    tests_require=[
        'pytest>=2.7.2',
        'mock',
        'mongomock'
    ],
)
