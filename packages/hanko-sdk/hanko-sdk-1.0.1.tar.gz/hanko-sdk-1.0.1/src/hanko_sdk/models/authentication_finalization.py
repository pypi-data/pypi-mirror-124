from dataclasses import dataclass
from typing import ClassVar

from enforce_typing import enforce_types

from .assertion import CredentialAssertionResponse, AuthenticatorAssertionResponse
from .base64_entities import UrlEncodedBase64
from .base_model import BaseModel
from .core import Credential
from .options import CredentialType
from .credential import PublicKeyCredential


@dataclass
class AuthenticationFinalizationRequest(CredentialAssertionResponse):
    """ Contains the representation of a :py:class:`PublicKeyCredential` obtained through assertion generation via the browsers' ``navigator.credentials.get()``.

        See also: https://www.w3.org/TR/webauthn-2/#publickeycredential """

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return AuthenticationFinalizationRequest(
            d.get(AuthenticationFinalizationRequest.ID_KEY, None),
            CredentialType.from_json_serializable(d.get(AuthenticationFinalizationRequest.TYPE_KEY, None)),
            UrlEncodedBase64.from_json_serializable(d.get(AuthenticationFinalizationRequest.RAW_ID_KEY, None)),
            d.get(AuthenticationFinalizationRequest.EXTENSIONS_KEY, None),
            AuthenticatorAssertionResponse.from_json_serializable(d.get(AuthenticationFinalizationRequest.ASSERTION_RESPONSE_KEY, None))
        )


@dataclass
class AuthenticationFinalizationResponse(BaseModel):
    """ Represents the response of a successful authentication. """

    credential: Credential
    CREDENTIAL_KEY: ClassVar[str] = "credential"

    def to_json_serializable_internal(self) -> dict:
        return {
            AuthenticationFinalizationResponse.CREDENTIAL_KEY: self.credential
        }

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return AuthenticationFinalizationResponse(
            Credential.from_json_serializable(d.get(AuthenticationFinalizationResponse.CREDENTIAL_KEY, None))
        )
