from abc import ABC, abstractmethod
from enum import Enum
from typing import Type, Optional, List
from requests import Request, Session, PreparedRequest

from . import json_serializer
from .auth import HankoAuth
from .config import HankoHttpClientConfig
import logging

from .exceptions.hanko_exceptions import HankoAuthenticationException, HankoNotFoundException, HankoUnexpectedException
from .models.authentication_finalization import AuthenticationFinalizationRequest, AuthenticationFinalizationResponse
from .models.authentication_initialization import AuthenticationInitializationRequest, \
    AuthenticationInitializationResponse
from .models.base_model import BaseModel
from .models.core import Credential
from .models.core import CredentialList
from .models.credential_query import CredentialQuery
from .models.credential_update import CredentialUpdateRequest
from .models.registration_finalization import RegistrationFinalizationRequest, RegistrationFinalizationResponse
from .models.registration_initialization import RegistrationInitializationRequest, RegistrationInitializationResponse
from .models.transaction_finalization import TransactionFinalizationRequest, TransactionFinalizationResponse
from .models.transaction_initialization import TransactionInitializationRequest, TransactionInitializationResponse
from .utils import url_utils


class BaseHankoClient(ABC):
    """ Defines the Hanko API interface. """

    @abstractmethod
    def initialize_registration(self, request: RegistrationInitializationRequest) -> RegistrationInitializationResponse:
        """ Initializes the registration of a new credential using a :py:class:`RegistrationInitializationRequest`.
            On successful initialization, the Hanko Authentication API returns a
            :py:class:`RegistrationInitializationResponse`. Send the response to your client application in order to
            pass it to the browser's WebAuthn API's ``navigator.credentials.create()`` function.

            :param request: The RegistrationInitializationRequest.
            :return: A RegistrationInitializationResponse object.
            """
        pass

    @abstractmethod
    def finalize_registration(self, request: RegistrationFinalizationRequest) -> RegistrationFinalizationResponse:
        """ Finalizes the registration request initiated by ``initialize_registration``. Provide a
            :py:class:`RegistrationFinalizationRequest` which represents the result of calling the browser's WebAuthn API's
            ``navigator.credentials.create()`` function.

            :param request: The RegistrationFinalizationRequest.
            :return: A RegistrationFinalizationResponse. """
        pass

    @abstractmethod
    def initialize_authentication(self, request: AuthenticationInitializationRequest) -> AuthenticationInitializationResponse:
        """ Initializes an authentication with a registered credential using an
            :py:class:`AuthenticationInitializationRequest`. On successful initialization, the Hanko Authentication API
            returns an :py:class:`AuthenticationInitializationResponse`. Send the response to your client application in
            order to pass it to the browser's WebAuthn API's ``navigator.credentials.get()`` function.

            :param request: The AuthenticationInitializationRequest.
            :return: An AuthenticationInitializationResponse. """
        pass

    @abstractmethod
    def finalize_authentication(self, request: AuthenticationFinalizationRequest) -> AuthenticationFinalizationResponse:
        """ Finalizes the authentication request initiated by ``initialize_authentication``. Provide
            an :py:class:`AuthenticationFinalizationRequest` which represents the result of calling the browser's
            WebAuthn API's ``navigator.credentials.get()`` function.

            :param request: The AuthenticationFinalizationRequest.
            :return: An AuthenticationFinalizationResponse. """
        pass

    @abstractmethod
    def initialize_transaction(self, request: TransactionInitializationRequest) -> TransactionInitializationResponse:
        """ Initiates a transaction. A transaction operation is analogous to the authentication operation,
            with the main difference being that a transaction context must be provided in the form of a string.
            This value will become part of the challenge an authenticator signs over during the operation.
            Initialize a transaction using a :py:class:`TransactionInitializationRequest`. On successful initialization,
            the Hanko Authentication API returns a :py:class:`TransactionInitializationResponse`. Send the response to
            your client application in order to pass it to the browser's WebAuthn API's
            ``navigator.credentials.get()`` function.

            :param request: The TransactionInitializationRequest.
            :return: A TransactionInitializationResponse. """
        pass

    @abstractmethod
    def finalize_transaction(self, request: TransactionFinalizationRequest) -> TransactionFinalizationResponse:
        """ Finalizes the transaction request initiated by ``initialize_transaction``. Provide a
            :py:class:`TransactionFinalizationRequest` which represents the result of calling of the browser's WebAuthn
            API's ``navigator.credentials.get()`` function.

            :param request: The TransactionFinalizationRequest.
            :return: A TransactionFinalizationResponse. """
        pass

    @abstractmethod
    def list_credentials(self, credential_query: CredentialQuery) -> List[Credential]:
        """ Returns a list of :py:class:`Credential`. Filter by ``user_id`` and paginate results using a
            :py:class:`CredentialQuery`. The value for ``page_size`` defaults to ``10`` and the value for
            ``page`` to ``1``.

            :param credential_query: The CredentialQuery.
            :return: A list of Credential objects. """
        pass

    @abstractmethod
    def get_credential(self, credential_id: str) -> Credential:
        """ Returns the :py:class:`Credential` with the specified ``credential_id``.

            :param credential_id: The id of the Credential to retrieve.
            :return: The Credential. """
        pass

    @abstractmethod
    def delete_credential(self, credential_id: str):
        """ Deletes the :py:class:`Credential` with the specified ``credential_id``.

            :param credential_id: The id of the credential to delete. """
        pass

    @abstractmethod
    def update_credential(self, credential_id: str, request: CredentialUpdateRequest) -> Credential:
        """ Updates the :py:class:`Credential` with the specified ``credential_id``. Provide a
            :py:class:`CredentialUpdateRequest` with the updated data. Currently, you can only update the name of a
            :py:class:`Credential`.

            :param credential_id: The id of the Credential to update.
            :param request: The CredentialUpdateRequest.
            :return: The updated Credential. """
        pass


class RequestMethod(Enum):

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class HankoHttpClient(BaseHankoClient):
    """ A HTTP implementation of :py:class:`BaseHankoClient`. """

    PATH_WEBAUTHN_BASE = "webauthn"
    PATH_REGISTRATION_INITIALIZE = "registration/initialize"
    PATH_REGISTRATION_FINALIZE = "registration/finalize"
    PATH_AUTHENTICATION_INITIALIZE = "authentication/initialize"
    PATH_AUTHENTICATION_FINALIZE = "authentication/finalize"
    PATH_TRANSACTION_INITIALIZE = "transaction/initialize"
    PATH_TRANSACTION_FINALIZE = "transaction/finalize"
    PATH_CREDENTIALS = "credentials"

    def __init__(self, config: HankoHttpClientConfig, logger: logging.Logger = None):
        """ Constructs a :py:class:`HankoHttpClient`.

            :param config: A Hanko configuration.
            :param logger: An optional Logger object. """

        self.__config = config
        self.__logger = logger
        self.__session = Session()

    def __del__(self):
        if self.__session is not None:
            self.__session.close()

    def __build_url(self, path: str) -> str:
        """ Builds an absolute Hanko API URL.

            :param path: The API endpoint path.
            :return: An absolute Hanko API URL. """

        return url_utils.build_url(self.__config.base_url, self.__config.api_version, HankoHttpClient.PATH_WEBAUTHN_BASE, path)

    def __prepare_request(self, request_path: str, method: RequestMethod, body: Optional[BaseModel], query_parameters: Optional[dict]) -> PreparedRequest:
        """ Creates and prepares a :py:class:`Request` object with the given parameters.

            :param request_path: The API endpoint path.
            :param method: The HTTP method to use for the request.
            :param body: The request body.
            :param query_parameters: The query parameters.
            :return: A PreparedRequest. """

        url = self.__build_url(request_path)

        body_json = None

        if body is not None:
            body_json = json_serializer.serialize(body)

        request = Request(method.value, url, data=body_json, auth=HankoAuth(self.__config, url_utils.remove_base(url, self.__config.base_url)), params=query_parameters)
        return request.prepare()

    def __log_request(self, request: PreparedRequest):
        """ Logs the request parameter using the ``logger``.

            :param request: The request to be logged. """

        if self.__logger is not None:
            self.__logger.info("-- BEGIN Hanko API Request --")
            self.__logger.info("request method: %s", request.method)
            self.__logger.info("request URL: %s", request.path_url)
            self.__logger.info("authorization: %s", request.headers.get("Authorization", "none"))
            self.__logger.info("body: %s", request.body)
            self.__logger.info("-- END Hanko API Request --")

    def __make_request(self, request_path: str, method: RequestMethod, body: Optional[BaseModel], query_parameters: Optional[dict], response_type: Optional[Type[BaseModel]]):
        """ Performs a HTTP request to the Hanko API with the given body and query parameters. Returns and deserializes
            the response as the given type ``response_type``.

            The body, if not null, is serialized to a JSON string using the ``json_serializer`` module.

            The query_parameters parameter, also optional, is used to build the request query parameters.

            :param request_path: The API endpoint path.
            :param method: The HTTP method to use for the request.
            :param body: The request body.
            :param query_parameters: The query parameters.
            :param response_type: The type the API response to be deserialized as.
            :return: The response body, deserialized as response_type. """

        request = self.__prepare_request(request_path, method, body, query_parameters)

        self.__log_request(request)

        response = self.__session.send(request)

        if response.ok:
            if response_type is not None and response.text is not None and len(response.text) > 0:
                response_object = json_serializer.deserialize_string(response.text, response_type)
                return response_object
            else:
                return None

        if response.status_code == 401:
            raise HankoAuthenticationException(response.text, response.status_code, request.path_url)
        elif response.status_code == 404:
            raise HankoNotFoundException(response.text, response.status_code, request.path_url)

        raise HankoUnexpectedException(response.text, response.status_code, request.path_url)

    def initialize_registration(self, request: RegistrationInitializationRequest) -> RegistrationInitializationResponse:
        response = self.__make_request(HankoHttpClient.PATH_REGISTRATION_INITIALIZE, RequestMethod.POST, request, None, RegistrationInitializationResponse)
        return response

    def finalize_registration(self, request: RegistrationFinalizationRequest) -> RegistrationFinalizationResponse:
        response = self.__make_request(HankoHttpClient.PATH_REGISTRATION_FINALIZE, RequestMethod.POST, request, None, RegistrationFinalizationResponse)
        return response

    def initialize_authentication(self, request: AuthenticationInitializationRequest) -> AuthenticationInitializationResponse:
        response = self.__make_request(HankoHttpClient.PATH_AUTHENTICATION_INITIALIZE, RequestMethod.POST, request, None, AuthenticationInitializationResponse)
        return response

    def finalize_authentication(self, request: AuthenticationFinalizationRequest) -> AuthenticationFinalizationResponse:
        response = self.__make_request(HankoHttpClient.PATH_AUTHENTICATION_FINALIZE, RequestMethod.POST, request, None, AuthenticationFinalizationResponse)
        return response

    def initialize_transaction(self, request: TransactionInitializationRequest) -> TransactionInitializationResponse:
        response = self.__make_request(HankoHttpClient.PATH_TRANSACTION_INITIALIZE, RequestMethod.POST, request, None, TransactionInitializationResponse)
        return response

    def finalize_transaction(self, request: TransactionFinalizationRequest) -> TransactionFinalizationResponse:
        response = self.__make_request(HankoHttpClient.PATH_TRANSACTION_FINALIZE, RequestMethod.POST, request, None, TransactionFinalizationResponse)
        return response

    def list_credentials(self, credential_query: CredentialQuery) -> List[Credential]:
        query_parameters = credential_query.to_json_serializable() if credential_query is not None else {}
        response: CredentialList = self.__make_request(HankoHttpClient.PATH_CREDENTIALS, RequestMethod.GET, None, query_parameters, CredentialList)

        return response.credentials if response is not None else []

    def get_credential(self, credential_id: str) -> Credential:
        path = "{}/{}".format(HankoHttpClient.PATH_CREDENTIALS, credential_id)
        response = self.__make_request(path, RequestMethod.GET, None, None, Credential)

        return response

    def delete_credential(self, credential_id: str):
        path = "{}/{}".format(HankoHttpClient.PATH_CREDENTIALS, credential_id)
        self.__make_request(path, RequestMethod.DELETE, None, None, None)

    def update_credential(self, credential_id: str, request: CredentialUpdateRequest) -> Credential:
        path = "{}/{}".format(HankoHttpClient.PATH_CREDENTIALS, credential_id)
        response = self.__make_request(path, RequestMethod.PUT, request, None, Credential)

        return response
