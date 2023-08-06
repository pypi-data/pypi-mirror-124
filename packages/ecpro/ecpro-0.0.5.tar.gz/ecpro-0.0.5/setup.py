# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @author :libo

from setuptools import setup

setup(
    name='ecpro',
    version='0.0.4',
    description='ecpro image crop utils',
    long_description='ecpro crop package',
    author='libo',
    author_email='6878595@qq.com',
    py_modules=['mySelfSum'],
    url='',
    license='MIT Licence',
    keywords='testing ecpro crop',
    platforms='any',
    python_requires='>=3.7.*',
    install_requires=[],
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      ],
)

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ecpro",
    version="0.0.5",
    author="libo",
    author_email="6878595@qq.com",
    description="ecpro image crop utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)