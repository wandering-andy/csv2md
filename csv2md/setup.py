# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="csv2mdpages",
    version="0.1.0",
    py_modules=["csv2mdpages"],
    install_requires=[
        "Click",
        "mdutils",
    ],
    entry_points={
        "console_scripts": [
            "csv2mdpages = csv2mdpages:convert",
        ],
    },
)
