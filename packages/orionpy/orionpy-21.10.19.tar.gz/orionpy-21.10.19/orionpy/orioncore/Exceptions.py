# coding=utf-8

# =============================================================================
# CLASS
# =============================================================================


class BuildFilterError(ValueError):
    """Exception class to raise if an error occurs while creating a filter"""

    def foo(self):
        pass


# =============================================================================
# CLASS
# =============================================================================


class FilteringValuesError(ValueError):
    """Exception class to raise if an error occurs while setting filtering values"""

    def foo(self):
        pass


# =============================================================================
# CLASS
# =============================================================================


class CSVError(ValueError):
    """Exception class to raise if an error occurs while setting filtering values"""

    def foo(self):
        pass


# =============================================================================
# CLASS
# =============================================================================


class RequestError(ValueError):
    """Exception class to raise if an error occurs while setting filtering values"""

    def foo(self):
        pass


# =============================================================================
# CLASS
# =============================================================================

    
class OrionAuthorizeError(ValueError):
    """Exception class to raise if a user not authorize to connect on orion"""
    def foo(self):
        pass
