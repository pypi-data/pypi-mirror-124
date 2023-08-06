"""
.. include:: ../README.md
"""

from .body import Body
from .head import Head
from .opml import OPML
from .outline import Outline

__version__ = "0.1.1"

# Export everything at the top-level.
__all__ = [
    "Body",
    "Head",
    "OPML",
    "Outline",
]

# Set docformat for pdoc.
__docformat__ = "restructuredtext"
