from dataclasses import dataclass

from enforce_typing import enforce_types

from ..utils import base64_utils

from .base_model import BaseModel


@dataclass
class UrlEncodedBase64(BaseModel):
    """ Represents an URL-encoded Base64 value. """

    content: bytes

    def to_json_serializable_internal(self):
        return base64_utils.urlsafe_b64encode_to_string(self.content, trim_padding=True)

    @classmethod
    def from_json_serializable(cls, s: str):
        if s is None:
            return None

        return UrlEncodedBase64(base64_utils.urlsafe_b64decode(s))

    @classmethod
    def from_utf8_string(cls, s: str):
        return UrlEncodedBase64(bytes(s, "utf-8"))
