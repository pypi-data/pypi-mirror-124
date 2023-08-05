from .base_model import BaseModel
from enum import Enum, unique


@unique
class AuthenticatorAttachment(BaseModel, Enum):
    """ Describes authenticators' attachment modalities. Relying Parties use this for two purposes:

    * to express a preferred authenticator attachment modality when calling ``navigator.credentials.create()`` to create a credential, and
    * to inform the client of the Relying Party's best belief about how to locate the managing authenticators of the credentials listed in allowCredentials when calling ``navigator.credentials.get()``.

    `Web Authentication Level 1 - 5.4.5. Authenticator Attachment Enumeration <https://www.w3.org/TR/webauthn-1/#attachment">`_

    """

    PLATFORM = "platform"
    """ Indicates platform attachment. """

    CROSS_PLATFORM = "cross-platform"
    """ Indicates cross-platform attachment."""

    def to_json_serializable_internal(self):
        return self.value

    @classmethod
    def from_json_serializable(cls, obj):
        if obj is None:
            return None

        return AuthenticatorAttachment(obj)


@unique
class UserVerificationRequirement(BaseModel, Enum):
    """ Represents the UserVerfication.

        A WebAuthn Relying Party may require user verification for some of its operations but not for others, and may use this type to express its needs.

        `See §5.10.6. User Verification Requirement Enumeration <https://www.w3.org/TR/webauthn/#userVerificationRequirement>`_ """

    REQUIRED = "required"
    """ User verification is required to create/release a credential. """

    PREFERRED = "preferred"
    """ User verification is preferred to create/release a credential. """

    DISCOURAGED = "discouraged"
    """ The authenticator should not verify the user for the credential. """

    def to_json_serializable_internal(self):
        return self.value

    @classmethod
    def from_json_serializable(cls, obj):
        if obj is None:
            return None

        return UserVerificationRequirement(obj)
