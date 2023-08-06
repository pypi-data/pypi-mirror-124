class Pv60hzBaseException(Exception):
    """
    Base class for all pv60hz's errors.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class DataRootNullException(Pv60hzBaseException):
    """
    Loader Data Root path Null Value Exception
    """

    def __init__(self, message="The value of data root must not be None."):
        self.message = message


class LatLonInvalidException(Pv60hzBaseException):
    """
    Latitude and Longitude Invalid Exception
    """

    def __init__(
        self,
        message="latitude must belongs to [-90, 90] and longitude must belongs to [-180, 180]",
    ):
        self.message = message


class EccodesRuntimeErrorException(Pv60hzBaseException):
    """
    Eccodes library must be installed.
    """

    def __init__(
        self,
        message="Eccodes library must be installed. Please check follow url: (https://github.com/ecmwf/cfgrib)",
    ):
        self.message = message
