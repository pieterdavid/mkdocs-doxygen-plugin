""" Setuptools-based setup module for mkdocs-doxygen-plugin

derived from the pypa example, see https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mkdocs-doxygen-plugin",

    version="0.1.0",

    description="Doxygen plugin for MkDocs",
    long_description=long_description,

    url="https://github.com/pieterdavid/mkdocs-doxygen-plugin",

    author="Pieter David",
    author_email="pieter.david@gmail.com",

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='doxygen mkdocs',

    packages=["mkdocsdoxygen"],

    install_requires=['mkdocs'],

    extras_require={},

    package_data={},
    data_files=[],

    entry_points={
        "mkdocs.plugins" : [
            "doxygen = mkdocsdoxygen.plugin:DoxygenPlugin"
        ]
    },
)
