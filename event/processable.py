import inspect
import itertools
import typing
from enum import Enum

class Processable:
    __id_iterators = {}
    __signiture_parameters = {}
    required_attributes: typing.List[str]
    
    def __init__(self) -> None:
        cls: typing.Type[Processable] = type(self)
        if cls not in self.__id_iterators:
            self.__id_iterators[cls] = itertools.count()
            self.__signiture_parameters[cls] = inspect.signature(cls).parameters
        self._id = next(self.__id_iterators[cls])

    def to_reduced_dict(self) -> dict:
        result = {'_id': self._id}
        for attribute_str in self.required_attributes:
            value = getattr(self, attribute_str)
            if value == self.__signiture_parameters[type(self)][attribute_str].default:
                continue

            if isinstance(value, Enum):
                result[attribute_str] = value.value
                continue
        
            if not isinstance(value, list):
                result[attribute_str] = value
                continue
           
            result[attribute_str] = []
            for sub_val in value:
                if issubclass(type(sub_val), Processable):
                    result[attribute_str].append(sub_val.to_reduced_dict())
                else:
                    result[attribute_str].append(sub_val)

        return result

    def update_from_dict(self, value_dict: dict) -> None:
        for key, val in value_dict.items():
            setattr(self, key, val)
