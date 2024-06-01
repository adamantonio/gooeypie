"""Setup script for Gooey Pie"""

import os.path
from setuptools import setup

# README
HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="gooeypie",
    version="0.12.0",
    description="Designed for beginners, GooeyPie is a simple but powerful GUI library.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gooeypie.dev",
    author="Adam Antonio",
    author_email="adam@gooeypie.dev",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ],
    packages=["gooeypie"],
    include_package_data=True,
    install_requires=["pillow"],
)
