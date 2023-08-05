
class HankoHttpClientConfig:
    """ Encapsulates the main configuration parameters for creating a HankoHttpClient. """

    DEFAULT_API_VERSION = "v1"

    def __init__(self, base_url, secret, api_key, api_version=DEFAULT_API_VERSION):
        """
            Constructs a HankoHttpClientConfig.

            :param base_url: The Hanko API base URL, must be a valid URL.
            :param secret: The Hanko API secret.
            :param api_key: The Hanko API key ID.
            :param api_version: The Hanko API version. Default is "v1".
        """
        self.__base_url = base_url
        self.__secret = secret
        self.__api_key = api_key
        self.__api_version = api_version

        if self.__api_version is None:
            self.__api_version = HankoHttpClientConfig.DEFAULT_API_VERSION

    @property
    def base_url(self) -> str:
        """ The Hanko API base URL. """
        return self.__base_url

    @property
    def secret(self) -> str:
        """ The Hanko API secret. """
        return self.__secret

    @property
    def api_key(self) -> str:
        """ The Hanko API key ID """
        return self.__api_key

    @property
    def api_version(self) -> str:
        """ The Hanko API version. """
        return self.__api_version
