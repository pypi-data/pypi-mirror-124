from dataclasses import dataclass
from typing import ClassVar, Optional

from enforce_typing import enforce_types

from .attestation import AuthenticatorAttestationResponse
from .base64_entities import UrlEncodedBase64
from .base_model import BaseModel
from .options import CredentialType


@dataclass
class Credential(BaseModel):
    """ The basic credential type.

        https://w3c.github.io/webappsec-credential-management/#credential """

    id: str
    """ The credential’s identifier. The requirements for the
        identifier are distinct for each type of credential. It might
        represent a username for username/password tuples, for example. """
    ID_KEY: ClassVar[str] = "id"

    type: CredentialType
    """ The value of the object’s interface object's ``type`` slot,
        which specifies the credential type represented by this object.
        This should be type ``PublicKey`` for Webauthn credentials."""
    TYPE_KEY: ClassVar[str] = "type"

    def to_json_serializable_internal(self) -> dict:
        return {
            Credential.ID_KEY: self.id,
            Credential.TYPE_KEY: self.type
        }

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return Credential(
            d.get(Credential.ID_KEY, None),
            CredentialType.from_json_serializable(d.get(Credential.TYPE_KEY, None))
        )


@dataclass
class PublicKeyCredential(Credential):
    """ Inherits from :py:class:`Credential`, and contains
        the attributes that are returned to the caller when a new credential
        is created, or a new assertion is requested. """

    raw_id: UrlEncodedBase64
    RAW_ID_KEY: ClassVar[str] = "rawId"

    extensions: Optional[dict]
    EXTENSIONS_KEY: ClassVar[str] = "extensions"

    def to_json_serializable_internal(self) -> dict:
        json_serializable = super().to_json_serializable_internal()
        json_serializable.update({
            PublicKeyCredential.RAW_ID_KEY: self.raw_id,
            PublicKeyCredential.EXTENSIONS_KEY: self.extensions
        })

        return json_serializable

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return PublicKeyCredential(
            d.get(PublicKeyCredential.ID_KEY, None),
            CredentialType.from_json_serializable(d.get(PublicKeyCredential.TYPE_KEY, None)),
            UrlEncodedBase64.from_json_serializable(d.get(PublicKeyCredential.RAW_ID_KEY, None)),
            d.get(PublicKeyCredential.EXTENSIONS_KEY, None)
        )


@dataclass
class CredentialCreationResponse(PublicKeyCredential):
    """ Inherits from :py:class:`PublicKeyCredential`. """
    attestation_response: Optional[AuthenticatorAttestationResponse] = None
    ATTESTATION_RESPONSE_KEY: ClassVar[str] = "response"

    def to_json_serializable_internal(self) -> dict:
        json_serializable = super().to_json_serializable_internal()
        json_serializable.update({
            CredentialCreationResponse.ATTESTATION_RESPONSE_KEY: self.attestation_response
        })

        return json_serializable

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return CredentialCreationResponse(
            d.get(CredentialCreationResponse.ID_KEY, None),
            CredentialType.from_json_serializable(d.get(CredentialCreationResponse.TYPE_KEY, None)),
            UrlEncodedBase64.from_json_serializable(d.get(CredentialCreationResponse.RAW_ID_KEY, None)),
            d.get(CredentialCreationResponse.EXTENSIONS_KEY, None),
            AuthenticatorAttestationResponse.from_json_serializable(d.get(CredentialCreationResponse.ATTESTATION_RESPONSE_KEY, None))
        )
