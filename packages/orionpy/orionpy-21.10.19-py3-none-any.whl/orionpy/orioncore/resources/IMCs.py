from orionpy.orioncore.resources.IMCResource import IMCResource
from ..Elements import Elements

import json


class IMCs(Elements):
    """
    Class allowing to get access to the list of business resource
    """

    def __init__(self):
        """Initialize and build our list of resources
        """
        super().__init__()

    # ----- All business resources in aOB -----
    def _update(self):
        """ Update the list of resources to make sure it's consistent with our database.
        """
        self._resources = []
        self._build_all()

    def _build_all(self):
        """Method to build a list with all resources
        """
        node_info_url = self.url_manager.imc_children_url()
        list_nodes = self.request.get_in_python(node_info_url)
        for node in list_nodes:
            if node["nodeType"] == "ResourceNode":
                resource_name = node["name"]
                self._add_resource_to_list(resource_name)

    def all(self):
        """
        :return: the list of elements values
        """
        # TODO convert to list ?
        self._update()
        return self._resources

    # ----- Geting 1 resource handled by aOB -----
    def get(self, element_name):
        """Look if a particular element exist.

        :param element_name: identification of element
        :return: required element or None if nothing found
        """
        element_name = element_name.strip()
        element = self._update_one(element_name)
        if element is None:
            print("[WARNING] element", element_name, "doesn't exist, None is returned")
            return None
        return element

    def _update_one(self, element_id):
        """Update one resource required

        :param element_id: REST access url of the resource
        :return: The resource if found. None otherwise"""
        return self._create_resource(element_id)

    # ----- Methods for creation of a resource instance -----
    def _add_resource_to_list(self, resource_name):
        """Creates an instance of a resource and add it to the appropiated list

        :param resource_name:
        :return:
        """
        resource_instance = self._create_resource(resource_name)
        if resource_instance is None:
            return
        self._resources.append(resource_instance)

    def _create_resource(self, resource_name):
        """Creates an instance of a IMC resource.

        :param resource_name:
        :return: The resource created or None if there was an error
        """
        resource_req = self._try_to_get_resource(resource_name)
        if resource_req is None or "error" in resource_req:
            print(resource_req)
            return None
        
        return IMCResource(resource_req)

    def _try_to_get_resource(self, resource_name):
        """(FIX) Try to get a service and handle exception if there is one."""
        service_req = None
        try:
            service_req = self.request.get_in_python(self.url_manager.imc_definition_url(resource_name))
        except Exception:
            service_req = None

        return service_req

    # --- Method to execute IMC
    def execute(self, imc_definition, input_set, out_sr = None):
        """Execute IMC with input parameters

        :param imc_definition: json imc definition
        :param input_set: json features used as input imc feature
        :return: required element or None if nothing found
        """
        # If output spatial reference not define, use the input spatial reference
        if not out_sr:
            out_sr = input_set.get("spatialReference")

        # Check if spatialReference attribute is supplied for all features
        for f in input_set.get("features"):
            if f.get("geometry") and not f.get("geometry").get("spatialReference"):
                f["geometry"]["spatialReference"] = input_set.get("spatialReference")

        feature_set = {"features": input_set}
        imc_result = self.request.post_in_python(self.url_manager.execute_imc_url(), data = {
            "imcDefinition": json.dumps(imc_definition), 
            "featureSet": json.dumps(feature_set), 
            "outSR": json.dumps(out_sr)})
        return imc_result