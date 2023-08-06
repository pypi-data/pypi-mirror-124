r"""
The torch.dml package contains data structures for multi-dimensional
tensors and defines mathematical operations over these tensors.
Additionally, it provides many utilities for efficient serializing of
Tensors and arbitrary types, and other useful utilities.

This is the DML counterpart, that enables you to run your tensor computations on DML.
"""

import os
import sys
import platform
import textwrap
import ctypes
import warnings

class DoubleStorage:
    pass


class FloatStorage:
    pass


class HalfStorage:
    pass


class LongStorage:
    pass


class IntStorage:
    pass


class ShortStorage:
    pass


class CharStorage:
    pass


class ULongStorage:
    pass


class UIntStorage:
    pass


class UShortStorage:
    pass


class ByteStorage:
    pass