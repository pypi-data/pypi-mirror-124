from typing import Type

from .models.base_model import BaseModel
import json


def serialize(model: BaseModel, sort_keys=False, omit_nones=True) -> str:
    """ Serializes the model as JSON.

        :param model: The model to be serialized.
        :param sort_keys: Whether the resulting JSON to have sorted keys or not. Default is False.
        :param omit_nones: Whether None objects should be omitted or not. Default is True.
        :return: The serialized model as JSON string. """

    return json.dumps(model.to_json_serializable(omit_nones=omit_nones), sort_keys=sort_keys)


def deserialize_string(json_string: str, t: Type[BaseModel]):
    """ Deserializes the JSON string as the given type.

        :param json_string: The string to be deserialized.
        :param t: The target deserialization type. It has to be a subtype of BaseModel.
        :return: The deserialized object of type t. """

    data = json.loads(json_string)
    return t.from_json_serializable(data)


def deserialize_file(file, t: Type[BaseModel]):
    """ Deserializes the JSON file as the given type.

        :param file: The file to be deserialized.
        :param t: The target deserialization type. It has to be a subtype of BaseModel.
        :return: The deserialized object of type t. """

    data = json.load(file)
    return t.from_json_serializable(data)
