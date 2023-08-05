from dataclasses import dataclass
from typing import ClassVar

from enforce_typing import enforce_types

from .base_model import BaseModel


@enforce_types
@dataclass
class CredentialUpdateRequest(BaseModel):
    """ Used for updating an existing credential. """

    name: str
    NAME_KEY: ClassVar[str] = "name"

    def to_json_serializable_internal(self) -> dict:
        return {
            CredentialUpdateRequest.NAME_KEY: self.name
        }

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return CredentialUpdateRequest(
            d.get(CredentialUpdateRequest.NAME_KEY, None)
        )
