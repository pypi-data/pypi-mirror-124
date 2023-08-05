from abc import abstractmethod
from collections.abc import Sequence


class BaseModel:
    """ The base class of all Hanko models. """

    @abstractmethod
    def to_json_serializable_internal(self):
        """ Maps the top-most model to a JSON-serializable format.

            :return: A JSON-serializable representation (dict, list or primitive type) possibly containing non-JSON-serializable attributes. """
        pass

    @classmethod
    @abstractmethod
    def from_json_serializable(cls, d):
        """ Constructs a model from the given JSON serializable.

            :param d: The JSON serializable to be used for constructing the model. The supported types are: (dict, list, tuple, str, int, float, None).
            :return: A model instance.
            """
        pass

    def to_json_serializable(self, omit_nones=True):
        """ Converts the model to a JSON-serializable format.

            :param omit_nones: Whether None objects should be omitted or not.
            :return: A JSON-serializable representation of the model. If the model is of primitive type, then a primitive is returned. If the model represents a sequence, a list is returned. Else, a dictionary is returned. """
        return self.map_to_json_serializable_if_not_none(self.to_json_serializable_internal(), omit_nones=omit_nones)

    @classmethod
    def from_json_serializable_sequence(cls, seq: Sequence):
        """ Constructs a sequence of models from the given JSON-serializable sequence.

            :param seq: The JSON-serializable sequence.
            :return: A list of model instances. """

        if seq is None:
            return None

        return [cls.from_json_serializable(item) for item in seq]

    @classmethod
    def map_to_json_serializable_if_not_none(cls, obj, omit_nones=True):
        """ Maps the object to a JSON-serializable format.

            :param obj: The object to be mapped to a JSON-serializable format.
            :param omit_nones: Whether None objects should be omitted or not.
            :return: A JSON-serializable representation of the object. If the object is of primitive type, then a primitive is returned. If the object represents a sequence, a list is returned. Else, a dictionary is returned."""
        if obj is None:
            return None

        elif isinstance(obj, BaseModel):
            return obj.to_json_serializable(omit_nones=omit_nones)
        elif isinstance(obj, dict):
            return {
                key: cls.map_to_json_serializable_if_not_none(value, omit_nones=omit_nones)
                for key, value in obj.items()
                if not omit_nones or value is not None
            }
        elif isinstance(obj, tuple) or isinstance(obj, list):
            return [
                cls.map_to_json_serializable_if_not_none(value, omit_nones=omit_nones)
                for value in obj
                if not omit_nones or value is not None
            ]
        else:
            return obj

