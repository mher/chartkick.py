from __future__ import absolute_import
import os

VERSION = (0, 4, 2)
__version__ = '.'.join(map(str, VERSION))


def js():
    "returns home directory of js"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'js')
