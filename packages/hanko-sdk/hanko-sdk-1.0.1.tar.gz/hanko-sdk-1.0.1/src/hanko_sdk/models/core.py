from dataclasses import dataclass
from typing import ClassVar, Optional, List, Sequence

from enforce_typing import enforce_types

from .attachment import AuthenticatorAttachment
from .base_model import BaseModel
from .datetime_model import DateTime


@enforce_types
@dataclass
class User(BaseModel):
    """ The base representation of a user on whose behalf registration and authentication are performed with the
        Hanko Authentication API."""

    id: str
    ID_KEY: ClassVar[str] = "id"

    name: Optional[str] = None
    NAME_KEY: ClassVar[str] = "name"

    display_name: Optional[str] = None
    DISPLAY_NAME_KEY: ClassVar[str] = "displayName"

    def to_json_serializable_internal(self) -> dict:
        return {
            User.ID_KEY: self.id,
            User.NAME_KEY: self.name,
            User.DISPLAY_NAME_KEY: self.display_name
        }

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return User(
            d.get(User.ID_KEY, None),
            d.get(User.NAME_KEY, None),
            d.get(User.DISPLAY_NAME_KEY, None)
        )


@enforce_types
@dataclass
class Authenticator(BaseModel):
    """ Holds information about the authenticator associated with a registered credential. """

    aaguid: Optional[str]
    AAGUID_KEY: ClassVar[str] = "aaguid"

    name: Optional[str]
    NAME_KEY: ClassVar[str] = "name"

    attachment: Optional[AuthenticatorAttachment]
    ATTACHMENT_KEY: ClassVar[str] = "attachment"

    def to_json_serializable_internal(self) -> dict:
        return {
            Authenticator.AAGUID_KEY: self.aaguid,
            Authenticator.NAME_KEY: self.name,
            Authenticator.ATTACHMENT_KEY: self.attachment
        }

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return Authenticator(
            d.get(Authenticator.AAGUID_KEY, None),
            d.get(Authenticator.NAME_KEY, None),
            AuthenticatorAttachment.from_json_serializable(d.get(Authenticator.ATTACHMENT_KEY, None))
        )


@dataclass
class Credential(BaseModel):
    """ Represents a credential. """

    id: str
    ID_KEY: ClassVar[str] = "id"

    created_at: DateTime
    CREATED_AT_KEY: ClassVar[str] = "createdAt"

    last_used: DateTime
    LAST_USED_KEY: ClassVar[str] = "lastUsed"

    name: str
    NAME_KEY: ClassVar[str] = "name"

    user_verification: bool
    USER_VERIFICATION_KEY: ClassVar[str] = "userVerification"

    is_resident_key: bool
    IS_RESIDENT_KEY_KEY: ClassVar[str] = "isResidentKey"

    authenticator: Authenticator
    AUTHENTICATOR_KEY: ClassVar[str] = "authenticator"

    user: User
    USER_KEY: ClassVar[str] = "user"

    def to_json_serializable_internal(self) -> dict:
        return {
            Credential.ID_KEY: self.id,
            Credential.CREATED_AT_KEY: self.created_at,
            Credential.LAST_USED_KEY: self.last_used,
            Credential.NAME_KEY: self.name,
            Credential.USER_VERIFICATION_KEY: self.user_verification,
            Credential.IS_RESIDENT_KEY_KEY: self.is_resident_key,
            Credential.AUTHENTICATOR_KEY: self.authenticator,
            Credential.USER_KEY: self.user
        }

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return Credential(
            d.get(Credential.ID_KEY, None),
            DateTime.from_json_serializable(d.get(Credential.CREATED_AT_KEY, None)),
            DateTime.from_json_serializable(d.get(Credential.LAST_USED_KEY, None)),
            d.get(Credential.NAME_KEY, None),
            d.get(Credential.USER_VERIFICATION_KEY, None),
            d.get(Credential.IS_RESIDENT_KEY_KEY, None),
            Authenticator.from_json_serializable(d.get(Credential.AUTHENTICATOR_KEY, None)),
            User.from_json_serializable(d.get(Credential.USER_KEY, None))
        )


@enforce_types
@dataclass
class CredentialList(BaseModel):
    """ Represents a list of credentials. """

    credentials: List[Credential]

    def to_json_serializable_internal(self):
        return self.credentials

    @classmethod
    def from_json_serializable(cls, seq: Sequence):
        if seq is None:
            return None

        return CredentialList(
            Credential.from_json_serializable_sequence(seq)
        )