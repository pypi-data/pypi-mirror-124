from dataclasses import dataclass
from typing import ClassVar, Optional

from enforce_typing import enforce_types

from .authenticator import AuthenticatorResponse
from .base64_entities import UrlEncodedBase64
from .credential import PublicKeyCredential
from .options import CredentialType


@dataclass
class AuthenticatorAssertionResponse(AuthenticatorResponse):
    """ Contains the raw authenticator assertion data. """

    authenticator_data: UrlEncodedBase64
    AUTHENTICATOR_DATA_KEY: ClassVar[str] = "authenticatorData"

    signature: UrlEncodedBase64
    SIGNATURE_KEY: ClassVar[str] = "signature"

    user_handle: Optional[UrlEncodedBase64]
    USER_HANDLE_KEY: ClassVar[str] = "userHandle"

    def to_json_serializable_internal(self) -> dict:
        json_serializable = super().to_json_serializable_internal()
        json_serializable.update({
            AuthenticatorAssertionResponse.AUTHENTICATOR_DATA_KEY: self.authenticator_data,
            AuthenticatorAssertionResponse.SIGNATURE_KEY: self.signature,
            AuthenticatorAssertionResponse.USER_HANDLE_KEY: self.user_handle
        })

        return json_serializable

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return AuthenticatorAssertionResponse(
            UrlEncodedBase64.from_json_serializable(d.get(AuthenticatorAssertionResponse.CLIENT_DATA_JSON_KEY, None)),
            UrlEncodedBase64.from_json_serializable(d.get(AuthenticatorAssertionResponse.AUTHENTICATOR_DATA_KEY, None)),
            UrlEncodedBase64.from_json_serializable(d.get(AuthenticatorAssertionResponse.SIGNATURE_KEY, None)),
            UrlEncodedBase64.from_json_serializable(d.get(AuthenticatorAssertionResponse.USER_HANDLE_KEY, None))
        )


@dataclass
class CredentialAssertionResponse(PublicKeyCredential):
    """ Represents the raw response returned from an authenticator when a credential for login/assertion is requested. """

    assertion_response: AuthenticatorAssertionResponse
    ASSERTION_RESPONSE_KEY: ClassVar[str] = "response"

    def to_json_serializable_internal(self) -> dict:
        json_serializable = super().to_json_serializable_internal()
        json_serializable.update({
            CredentialAssertionResponse.ASSERTION_RESPONSE_KEY: self.assertion_response
        })

        return json_serializable

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return CredentialAssertionResponse(
            d.get(CredentialAssertionResponse.ID_KEY, None),
            CredentialType.from_json_serializable(d.get(CredentialAssertionResponse.TYPE_KEY, None)),
            UrlEncodedBase64.from_json_serializable(d.get(CredentialAssertionResponse.RAW_ID_KEY, None)),
            d.get(CredentialAssertionResponse.EXTENSIONS_KEY, None),
            AuthenticatorAssertionResponse.from_json_serializable(d.get(CredentialAssertionResponse.ASSERTION_RESPONSE_KEY, None))
        )
