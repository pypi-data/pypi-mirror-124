
# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

from setuptools import setup

setup(
    name = "password-portal",
    packages = ["password_portal"],
    entry_points = {
        "console_scripts": ['password-portal = password_portal.server:main']
        },
    version = '0.0.0',
    description = "password-portal flask",
    long_description = "HTTP RESTful interface for asymmetric and symmetric encryption",
    author = "Karl Rink",
    author_email = "karl@rink.us",
    url = "https://gitlab.com/krink/password-portal",
    install_requires = [ 'flask', 'flask-cors' ]
    )


