#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask application configuration module.

__author__ = "Aleksei Seliverstov"
__license__ = "MIT"
__email__ = "alexseliverstov@yahoo.com"
"""
import os


class Config(object):
    """
    Flask application configuration object class
    """
    SECRET_KEY = os.urandom(32)
