"""
Author: Greg Phillips

Version: 2022-02-04
"""

from enum import Enum, auto


class PrimitiveType(Enum):
    """
    The primitive types defined for the Nimble language, plus the error type.
    """
    Int = auto()
    Bool = auto()
    String = auto()
    ERROR = auto()

    def __str__(self):
        return self.name
