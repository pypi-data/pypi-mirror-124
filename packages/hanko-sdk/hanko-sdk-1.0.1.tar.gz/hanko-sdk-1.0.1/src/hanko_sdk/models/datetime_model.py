import datetime
from dataclasses import dataclass

from enforce_typing import enforce_types

from .base_model import BaseModel
from dateutil import parser


@enforce_types
@dataclass
class DateTime(BaseModel):
    """ Wraps a :py:class:`datetime.datetime` object, and implements JSON serialization/deserialization. """

    value: datetime.datetime

    def to_json_serializable_internal(self):
        return self.value.astimezone(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

    @classmethod
    def from_json_serializable(cls, d: str):
        if d is None:
            return None

        return DateTime(
            parser.parse(d)
        )
