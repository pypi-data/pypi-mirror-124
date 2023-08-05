# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

from .Geonote import Geonote
from .Items import Items

# =============================================================================
# CLASS
# =============================================================================


class Geonotes(Items):
    def __init__(self):
        super().__init__(
            "Feature Collection", "aob_geonote", lambda data: Geonote(data)
        )
