# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

from enum import Enum
from getpass import getpass
from orionpy.orioncore.OrionBase import OrionBase
from orionpy.orioncore.resources.IMCs import IMCs
from orionpy.orioncore.Exceptions import OrionAuthorizeError

from . import cfg_global
from .features.Geonotes import Geonotes
from .features.Projects import Projects
from .Filters import Filters
from .Groups import Groups
from .RequestManager import RequestManager
from .resources.Businesses import Businesses
from .resources.Services import Services
from .UrlBuilder import UrlBuilder
from .Users import Users

# =============================================================================
# CLASS
# =============================================================================


class OrionRest(OrionBase):
    # TODO check if Orion should really be a Singleton !
    # TODO get Orion/Portal version (/orion/version)
    """A singleton class. The main class of our project"""

    def __init__(
        self, username, password, url_machine, portal="portal", verify_cert=True
    ):
        super().__init__(username, password, url_machine, portal, verify_cert)
        
        self._projects = Projects()
        self._geonotes = Geonotes()
