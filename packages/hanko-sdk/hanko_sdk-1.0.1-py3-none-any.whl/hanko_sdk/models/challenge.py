from dataclasses import dataclass

from enforce_typing import enforce_types

from ..utils import base64_utils

from .base_model import BaseModel


@dataclass
class Challenge(BaseModel):
    """ Represents the challenge that should be signed and returned by the authenticator. """

    challenge_bytes: bytes

    def to_json_serializable_internal(self):
        return base64_utils.urlsafe_b64encode_to_string(self.challenge_bytes, trim_padding=True)

    @classmethod
    def from_json_serializable(cls, obj):
        if obj is None:
            return None

        return Challenge(base64_utils.urlsafe_b64decode(obj))

    @classmethod
    def from_utf8_string(cls, s: str):
        return Challenge(bytes(s, "utf-8"))

    def __str__(self) -> str:
        return self.to_json_serializable_internal()
