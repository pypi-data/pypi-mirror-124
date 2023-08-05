from dataclasses import dataclass
from enum import Enum, unique
from typing import ClassVar

from enforce_typing import enforce_types

from .base64_entities import UrlEncodedBase64
from .base_model import BaseModel


@unique
class AuthenticatorTransport(BaseModel, Enum):
    """ Defines the transport of Authenticators.

        Authenticators may implement various transports for communicating with clients. This enumeration defines
        hints as to how clients might communicate with a particular authenticator in order to obtain an assertion
        for a specific credential. Note that these hints represent the WebAuthn Relying Party's best belief as to
        how an authenticator may be reached. A Relying Party may obtain a list of transports hints from some
        attestation statement formats or via some out-of-band mechanism; it is outside the scope of this
        specification to define that mechanism.

        `See §5.10.4. Authenticator Transport <https://www.w3.org/TR/webauthn/#transport>`_ """

    USB = "usb"
    """ The authenticator should transport information over USB. """

    NFC = "nfc"
    """ The authenticator should transport information over Near Field Communication Protocol. """

    BLE = "ble"
    """ The authenticator should transport information over Bluetooth. """

    INTERNAL = "internal"
    """ The client should use an internal source like a TPM or SE. """

    def to_json_serializable_internal(self):
        return self.value

    @classmethod
    def from_json_serializable(cls, obj):
        if obj is None:
            return None

        return AuthenticatorTransport(obj)


@enforce_types
@dataclass
class AuthenticatorResponse(BaseModel):
    """ Authenticators respond to Relying Party requests by returning an object derived from the AuthenticatorResponse class.

        `See §5.2. Authenticator Responses <https://www.w3.org/TR/webauthn/#iface-authenticatorresponse>`_ """

    client_data_json: UrlEncodedBase64
    CLIENT_DATA_JSON_KEY: ClassVar[str] = "clientDataJSON"

    def to_json_serializable_internal(self) -> dict:
        return {
            AuthenticatorResponse.CLIENT_DATA_JSON_KEY: self.client_data_json
        }

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return AuthenticatorResponse(
            UrlEncodedBase64.from_json_serializable(d.get(AuthenticatorResponse.CLIENT_DATA_JSON_KEY, None))
        )
