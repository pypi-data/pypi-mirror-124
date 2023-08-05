from dataclasses import dataclass
from typing import ClassVar

from enforce_typing import enforce_types

from .authenticator import AuthenticatorResponse
from .base64_entities import UrlEncodedBase64


@enforce_types
@dataclass
class AuthenticatorAttestationResponse(AuthenticatorResponse):
    """ The initial unpacked 'response' object received by the relying party. """

    attestation_object: UrlEncodedBase64
    ATTESTATION_OBJECT_KEY: ClassVar[str] = "attestationObject"

    def to_json_serializable_internal(self) -> dict:
        json_serializable = super().to_json_serializable_internal()
        json_serializable.update({
            AuthenticatorAttestationResponse.ATTESTATION_OBJECT_KEY: self.attestation_object
        })

        return json_serializable

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return AuthenticatorAttestationResponse(
            UrlEncodedBase64.from_json_serializable(d.get(AuthenticatorAttestationResponse.CLIENT_DATA_JSON_KEY, None)),
            UrlEncodedBase64.from_json_serializable(d.get(AuthenticatorAttestationResponse.ATTESTATION_OBJECT_KEY, None))
        )
