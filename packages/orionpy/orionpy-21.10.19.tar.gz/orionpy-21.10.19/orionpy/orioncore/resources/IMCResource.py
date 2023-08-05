import abc

from ..RequestManager import RequestManager
from ..UrlBuilder import UrlBuilder


# TODO : factorize with Resource !
class IMCResource(metaclass = abc.ABCMeta):
    def __init__(self, resource_description):
        """

        :param resource_description: Description json of resource
        """
        self.id = resource_description.get("_id")
        self.name = resource_description.get("name")
        self.description = resource_description.get("description")
        self.definition = resource_description.get("definition")
        self._url_builder = UrlBuilder()
        self._request_mgr = RequestManager()

    def __str__(self):
        """Provides a string representation of a cadastre resource"""
        resource_str = "Resource name : {}".format(self.name)
        return resource_str
