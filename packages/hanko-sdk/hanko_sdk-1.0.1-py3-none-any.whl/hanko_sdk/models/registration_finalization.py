from dataclasses import dataclass
from typing import ClassVar

from enforce_typing import enforce_types

from .attestation import AuthenticatorAttestationResponse
from .base64_entities import UrlEncodedBase64
from .base_model import BaseModel
from .core import Credential
from .credential import CredentialCreationResponse
from .options import CredentialType


@enforce_types
@dataclass
class RegistrationFinalizationRequest(CredentialCreationResponse):
    """ Contains the representation of a ``PublicKeyCredential`` obtained through credential
        creation via the browsers' ``navigator.credentials.create()``.

        See also: https://www.w3.org/TR/webauthn-2/#publickeycredential """

    @classmethod
    def from_json_serializable(cls, d):
        return RegistrationFinalizationRequest(
            d.get(RegistrationFinalizationRequest.ID_KEY, None),
            CredentialType.from_json_serializable(d.get(RegistrationFinalizationRequest.TYPE_KEY, None)),
            UrlEncodedBase64.from_json_serializable(d.get(RegistrationFinalizationRequest.RAW_ID_KEY, None)),
            d.get(RegistrationFinalizationRequest.EXTENSIONS_KEY, None),
            AuthenticatorAttestationResponse.from_json_serializable(d.get(RegistrationFinalizationRequest.ATTESTATION_RESPONSE_KEY, None))
        )


@dataclass
class RegistrationFinalizationResponse(BaseModel):
    """ Represents the response of a successful credential registration. """

    credential: Credential
    CREDENTIAL_KEY: ClassVar[str] = "credential"

    def to_json_serializable_internal(self) -> dict:
        return {
            RegistrationFinalizationResponse.CREDENTIAL_KEY: self.credential
        }

    @classmethod
    def from_json_serializable(cls, d):
        if d is None:
            return None

        return RegistrationFinalizationResponse(
            Credential.from_json_serializable(d.get(RegistrationFinalizationResponse.CREDENTIAL_KEY, None))
        )
