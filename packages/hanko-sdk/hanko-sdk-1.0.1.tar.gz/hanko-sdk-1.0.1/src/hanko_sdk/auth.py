from requests import models
from requests.auth import AuthBase

from .config import HankoHttpClientConfig
from .utils import hmac_utils


class HankoAuth(AuthBase):
    """ Represents a Hanko request authenticator. """

    def __init__(self, config: HankoHttpClientConfig, request_path: str):
        """ Constructs a HankoAuth object.

            :param config: The Hanko config.
            :param request_path: The path of the request to be authenticated. """

        self.__config = config
        self.__request_path = request_path

    def __call__(self, r: models.PreparedRequest) -> models.PreparedRequest:
        """ Generates an authorization header for the given request based on the Hanko config.
            If the config contains an API key, then a HMAC value is calculated. Else, the API secret is used.

            :param r: The request.
            :return: The request, authenticated with an Authorization header. """

        if self.__config.api_key is not None and len(self.__config.api_key) > 0:
            hmac = hmac_utils.calculate_hmac(self.__config.api_key, self.__config.secret, r.method, self.__request_path, r.body)
            header_value = "hanko {}".format(hmac)
        else:
            header_value = "secret {}".format(self.__config.secret)

        r.headers["Authorization"] = header_value

        return r
