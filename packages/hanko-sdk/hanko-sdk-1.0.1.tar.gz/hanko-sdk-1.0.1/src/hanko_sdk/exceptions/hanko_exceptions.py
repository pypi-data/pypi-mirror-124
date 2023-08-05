
class HankoApiException(Exception):
    """Represents errors that occur when the Hanko API does not respond with a status code in the range 2xx."""

    def __init__(self, message: str, content: str, status_code: int, request_path: str):
        """ Constructs a new HankoApiException.

            :param message: The detail message.
            :param content: The Hanko API response content.
            :param status_code: The Hanko API HTTP response status.
            :param request_path: The original request path. """
        super(Exception, self).__init__(message)

        self.__content = content
        self.__status_code = status_code
        self.__request_path = request_path

    @property
    def content(self) -> str:
        """ The Hanko API response content. """
        return self.__content

    @property
    def status_code(self) -> int:
        """ The Hanko API HTTP response status. """
        return self.__status_code

    @property
    def request_path(self) -> str:
        """ The original request path. """
        return self.__request_path


class HankoAuthenticationException(HankoApiException):
    """ Represents errors that occur when requests to the Hanko API cannot be authenticated (i.e. have a 401 status code). """

    def __init__(self, content: str, status_code: int, request_path: str):
        """ Constructs a new HankoAuthenticationException.

            :param content: The Hanko API response content.
            :param status_code: The Hanko API HTTP response status.
            :param request_path: The original request path. """
        super(HankoAuthenticationException, self).__init__("Hanko API returned 401, please check your API key configuration", content, status_code, request_path)


class HankoNotFoundException(HankoApiException):
    """ Represents erros that occur when requested resources are not found by the Hanko API (i.e. if it response with a 404 status code)."""

    def __init__(self, content: str, status_code: int, request_path: str):
        """ Constructs a new HankoNotFoundException.

            :param content: The Hanko API response content.
            :param status_code: The Hanko API HTTP response status.
            :param request_path: The original request path. """
        super(HankoNotFoundException, self).__init__("Hanko API resource '{0}' not found.".format(request_path), content, status_code, request_path)


class HankoUnexpectedException(HankoApiException):
    """ Represents unexpected Hanko API errors. """

    def __init__(self, content: str, status_code: int, request_path: str):
        """ Constructs a new HankoUnexpectedException.

            :param content: The Hanko API response content.
            :param status_code: The Hanko API HTTP response status.
            :param request_path: The original request path. """
        super(HankoUnexpectedException, self).__init__("Hanko API returned an unexpected status code: {0}".format(request_path), content, status_code, request_path)
