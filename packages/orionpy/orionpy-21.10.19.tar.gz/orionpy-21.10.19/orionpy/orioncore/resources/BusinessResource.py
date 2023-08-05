# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import abc

from ..RequestManager import RequestManager
from ..UrlBuilder import UrlBuilder

# import json
# from .Resource import RightLevel


# =============================================================================
# NOTES
# =============================================================================

# https://integration.arcopole.fr/Orion/orion/admin/tree/object/BUSINESS/Cadastre

# =============================================================================
# CLASS
# =============================================================================

# TODO : factorize with Resource !
class BusinessResource(metaclass=abc.ABCMeta):
    def __init__(self, resource_description):
        """

        :param resource_description: Description json of resource
        """
        self.id = (
            resource_description.get("_id")
            or resource_description.get("id")
            or resource_description.get("name")
        )
        self._url_builder = UrlBuilder()
        self._request_mgr = RequestManager()
        self._description = resource_description

    def __str__(self):
        """Provides a string representation of a cadastre resource"""
        resource_str = "Resource id : {}".format(self.id)
        return resource_str
