from dataclasses import dataclass
from typing import ClassVar, Optional

from enforce_typing import enforce_types

from .base64_entities import UrlEncodedBase64
from .base_model import BaseModel


@enforce_types
@dataclass
class CredentialEntity(BaseModel):
    """ Describes a user account, or a WebAuthn Relying Party, with which a public key credential is associated.

        `See §5.4.1 <https://www.w3.org/TR/webauthn/#dictionary-pkcredentialentity>`_"""

    name: str
    """ A human-palatable name for the entity. Its function depends on what the credential represents:
        When inherited by ``RelyingPartyEntity`` it is a human-palatable identifier for the Relying Party,
        intended only for display. For example, \"ACME Corporation\", \"Wonderful Widgets, Inc.\" or \"ОАО Примертех\".
        
        When inherited by ``UserEntity``, it is a human-palatable identifier for a user account. It is
        intended only for display, i.e., aiding the user in determining the difference between user accounts with similar
        displayNames. For example, \"alexm\", \"alex.p.mueller@example.com\" or \"+14255551234\". """
    NAME_KEY: ClassVar[str] = "name"

    icon: Optional[str]
    """ A serialized URL which resolves to an image associated with the entity. For example,
        this could be a user’s avatar or a Relying Party's logo. This URL MUST be an a priori
        authenticated URL. Authenticators MUST accept and store a 128-byte minimum length for
        an icon member’s value. Authenticators MAY ignore an icon member’s value if its length
        is greater than 128 bytes. The URL’s scheme MAY be "data" to avoid fetches of the URL,
        at the cost of needing more storage. """
    ICON_KEY: ClassVar[str] = "icon"

    def to_json_serializable_internal(self):
        return {
            CredentialEntity.NAME_KEY: self.name,
            CredentialEntity.ICON_KEY: self.icon
        }

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return CredentialEntity(
            d.get(CredentialEntity.NAME_KEY, None),
            d.get(CredentialEntity.ICON_KEY, None)
        )


@enforce_types
@dataclass
class RelyingPartyEntity(CredentialEntity):
    """ Used to supply additional
        Relying Party attributes when creating a new credential.

        `See §5.4.2 <https://www.w3.org/TR/webauthn/#sctn-rp-credential-params>`_ """

    id: str
    ID_KEY: ClassVar[str] = "id"

    def to_json_serializable_internal(self):
        json_serializable = super().to_json_serializable_internal()
        json_serializable.update({
            RelyingPartyEntity.ID_KEY: self.id
        })

        return json_serializable

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return RelyingPartyEntity(
            d.get(RelyingPartyEntity.NAME_KEY, None),
            d.get(RelyingPartyEntity.ICON_KEY, None),
            d.get(RelyingPartyEntity.ID_KEY, None)
        )


@enforce_types
@dataclass
class UserEntity(CredentialEntity):
    """ Used to supply additional user account attributes when creating a new credential.
        `See §5.4.3 <https://www.w3.org/TR/webauthn/#sctn-user-credential-params>`_ """

    display_name: str
    """ A human-palatable name for the user account, intended only for display.
        For example, \"Alex P. Müller\" or \"田中 倫\". The Relying Party SHOULD let
        the user choose this, and SHOULD NOT restrict the choice more than necessary. """
    DISPLAY_NAME_KEY: ClassVar[str] = "displayName"

    id: UrlEncodedBase64
    """ The user handle of the user account entity. To ensure secure operation,
        authentication and authorization decisions MUST be made on the basis of this id
        member, not the displayName nor name members.
         
        See `Section 6.1 of [RFC8266] <https://www.w3.org/TR/webauthn/#biblio-rfc8266>`_ """
    ID_KEY: ClassVar[str] = "id"

    def to_json_serializable_internal(self) -> dict:
        json_serializable = super().to_json_serializable_internal()
        json_serializable.update({
            UserEntity.DISPLAY_NAME_KEY: self.display_name,
            UserEntity.ID_KEY: self.id
        })

        return json_serializable

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return UserEntity(
            d.get(UserEntity.NAME_KEY, None),
            d.get(UserEntity.ICON_KEY, None),
            d.get(UserEntity.DISPLAY_NAME_KEY, None),
            UrlEncodedBase64.from_json_serializable(d.get(UserEntity.ID_KEY, None))
        )

