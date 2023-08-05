from dataclasses import dataclass
from typing import ClassVar, Optional

from enforce_typing import enforce_types

from .base_model import BaseModel


@enforce_types
@dataclass
class CredentialQuery(BaseModel):
    """ Used for credential searches. """

    user_id: str
    USER_ID_KEY: ClassVar[str] = "user_id"

    page_size: Optional[int] = None
    PAGE_SIZE_KEY: ClassVar[str] = "page_size"

    page: Optional[int] = None
    PAGE_KEY: ClassVar[str] = "page"

    def to_json_serializable_internal(self) -> dict:
        return {
            CredentialQuery.USER_ID_KEY: self.user_id,
            CredentialQuery.PAGE_SIZE_KEY: self.page_size,
            CredentialQuery.PAGE_KEY: self.page
        }

    @classmethod
    def from_json_serializable(cls, d: dict):
        if d is None:
            return None

        return CredentialQuery(
            d.get(CredentialQuery.USER_ID_KEY, None),
            d.get(CredentialQuery.PAGE_SIZE_KEY, None),
            d.get(CredentialQuery.PAGE_KEY, None)
        )
