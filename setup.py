#! /usr/bin/env python

# SOAD Project
# copyright (C) 2020
from setuptools import setup


if __name__ == "__main__":
    setup(
        name="SOAD Project",
        version="0.0.1",
        author="SOAD Project",
        author_email="abc@iiits.in",
        url="https://github.com/hrs2203/soad_project_2020",
        packages=["soad_project"],
        install_requires=["numpy", "scipy"],
        extras_require={"dev": ["pytest"]},
    )
