# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

from enum import Enum
from getpass import getpass
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
# NOTES
# =============================================================================

# TODO use lazy_property !

# def _lazy_property(fn):
#     '''Decorator that makes a property lazy-evaluated.
#     '''
#     # http://stevenloria.com/lazy-evaluated-properties-in-python/
#     attr_name = '_lazy_' + fn.__name__

#     @property
#     @functools.wraps(fn)
#     def _lazy_property(self):
#         if not hasattr(self, attr_name):
#             setattr(self, attr_name, fn(self))
#         return getattr(self, attr_name)
#     return _lazy_property

#     @_lazy_property
#     def users(self):
#         The resource manager for GIS users.
#         return UserManager(self)


# =============================================================================
# CLASS
# =============================================================================


class _Singleton(type):
    """
    metaclass of Orion.
    type is the base metaclass
    """

    _instances = {}  # type: dict

    def __call__(cls, *args, **kwargs):
        """Method called when create a Singleton

        :param args: list of arguments
        :param kwargs: Dictionary [keyword arguments]= values of these arguments
        :return: the singleton instance of the class
        """
        # If the class was not created yet (not in our list)...
        if cls not in cls._instances:
            # call the __call__ method of type. So, calls the class constructor
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
            print("Connection to Orion successful !")
        else:
            print("Orion is a Singleton, a new creation is not possible")
        return cls._instances[cls]


# =============================================================================
# CLASS
# =============================================================================


class OrionKeys(Enum):
    config_key = "configs"
    federated_key = "federated"
    token_key = "token"


# =============================================================================
# CLASS
# =============================================================================


class OrionBase(metaclass=_Singleton):
    # TODO check if Orion should really be a Singleton !
    # TODO get Orion/Portal version (/orion/version)
    """A singleton class. The main class of our project"""

    def __init__(
        self, username, password, url_machine, portal="portal", verify_cert=True
    ):
        """Connect to orion and initialize required parameters

        :param username: valid username to get access to Orion
        :param password: valid password to get access to Orion.
            If empty string, will be asked securely.
        :param url_machine: Url of the machine to get access to Orion
        :param portal: optional string access to the portal
        :param verify_cert: optional boolean to say if add SSL verification or not
        """
        self.request = RequestManager(verify=verify_cert)
        self.url_manager = UrlBuilder(url_machine, portal=portal)
        token_url = self.url_manager.token_url()
        if not password:
            password = getpass("Saisir le mot de passe pour {} : ".format(username))
        self.token = self._generate_token(
            username, password, token_url, referer=url_machine
        )
        # Set the token of request manager (required for further requests)
        self.request.set_token(self.token)

        # Set if federated or not
        url = self.url_manager.aob_config_url()
        config = self.request.get_in_python(url)[OrionKeys.config_key.value]
        cfg_global.is_federated = config[0][OrionKeys.federated_key.value]


    @property
    def filters(self):
        """
        :return: List of filters in Orion
        """
        if hasattr(self, '_filters'):
            return self._filters
        return None

    @property
    def services(self):
        """
        :return: List of services (managed by Orion)
        """
        if hasattr(self, '_services'):
            return self._services
        return None

    @property
    def businesses(self):
        """
        :return: List of business (managed by Orion)
        """
        if hasattr(self, '_businesses'):
            return self._businesses
        return None

    @property
    def imcs(self):
        """
        :return: List of imc
        """
        if hasattr(self, '_imcs'):
            return self._imcs
        return None

    @property
    def groups(self):
        """
        :return: List of groups in Orion
        """
        if hasattr(self, '_groups'):
            return self._groups
        return None

    @property
    def projects(self):
        """
        Allow to call methods on class 'projects'
        :return: instance of the class 'projects'
        """
        if hasattr(self, '_projects'):
            return self._projects
        return None

    @property
    def geonotes(self):
        """
        Allow to call methods on class 'geonotes'
        :return: instance of the class 'geonotes'
        """
        if hasattr(self, '_geonotes'):
            return self._geonotes
        return None

    @property
    def users(self):
        """
        :return: List of users in Orion
        """
        if hasattr(self, '_users'):
            return self._users
        return None

    def is_federated(self):
        """
        Check if the ArcGIS installed is federated or not.
        :return: True if ArcGIS Federated, false otherwise
        """
        return cfg_global.is_federated

    def _generate_token(
        self,
        username,
        password,
        token_url,
        referer="http://www.esrifrance.fr",
        output="json",
    ):
        """If orion requires a secured connection, generates the token

        :param output: the output format expected
        :param referer: where to look for the token
        :param token_url: url to generate the token
        :return: the token generated
        """
        login_info = {
            "username": username,
            "password": password,
            "referer": referer,
            "f": output,
        }
        get_token = self.request.post(token_url, login_info, False)
        token_info = self.request.get_python_answer(get_token)
        return token_info[OrionKeys.token_key.value]
