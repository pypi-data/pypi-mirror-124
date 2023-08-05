from dataclasses import dataclass

from enforce_typing import enforce_types

from .assertion import AuthenticatorAssertionResponse
from .authentication_finalization import AuthenticationFinalizationRequest, AuthenticationFinalizationResponse
from .base64_entities import UrlEncodedBase64
from .core import Credential
from .options import CredentialType


@dataclass
class TransactionFinalizationRequest(AuthenticationFinalizationRequest):
    """ Contains the representation of a ``PublicKeyCredential`` obtained through assertion
        generation via the browsers' ``navigator.credentials.get()``.

        See also: https://www.w3.org/TR/webauthn-2/#publickeycredential """

    @classmethod
    def from_json_serializable(cls, d: dict):
        return TransactionFinalizationRequest(
            d.get(TransactionFinalizationRequest.ID_KEY, None),
            CredentialType.from_json_serializable(d.get(TransactionFinalizationRequest.TYPE_KEY, None)),
            UrlEncodedBase64.from_json_serializable(d.get(TransactionFinalizationRequest.RAW_ID_KEY, None)),
            d.get(TransactionFinalizationRequest.EXTENSIONS_KEY, None),
            AuthenticatorAssertionResponse.from_json_serializable(d.get(TransactionFinalizationRequest.ASSERTION_RESPONSE_KEY, None))
        )


@dataclass
class TransactionFinalizationResponse(AuthenticationFinalizationResponse):
    """ Represents the response of a successful transaction. """

    @classmethod
    def from_json_serializable(cls, d: dict):
        return TransactionFinalizationResponse(
            Credential.from_json_serializable(d.get(TransactionFinalizationResponse.CREDENTIAL_KEY, None))
        )
