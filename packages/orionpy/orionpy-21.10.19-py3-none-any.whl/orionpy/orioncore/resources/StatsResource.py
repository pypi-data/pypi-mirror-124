# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

from .BusinessResource import BusinessResource

# =============================================================================
# NOTES
# =============================================================================

# https://integration.arcopole.fr/Orion/orion/admin/tree/object/BUSINESS/Cadastre
# TODO : factorize with Resource !

# =============================================================================
# CLASS
# =============================================================================


class StatsResource(BusinessResource):
    def __init__(self, resource_description):
        """

        :param resource_description: Description of the stat resource
        """
        super().__init__(resource_description)
