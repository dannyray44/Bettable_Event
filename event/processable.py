from __future__ import annotations

import enum
import inspect
import itertools
import json
import typing

_child_values_dict: typing.Dict[typing.Type['Processable'], typing.Tuple[itertools.count, typing.Mapping[str, inspect.Parameter]]] = {}

class Processable:
    _required_attributes: typing.List[str] = []
    
    def __init__(self) -> None:
        cls: typing.Type[Processable] = type(self)
        if cls not in _child_values_dict:
            _child_values_dict[cls] = (
                itertools.count(),
                inspect.signature(cls).parameters
                )
        self.__id = next(_child_values_dict[cls][0])

    def to_json(self) -> str:
        return json.dumps(self, default=__ProcessableEncoder)
    
    #TODO: def update_self_from_json

    @classmethod
    def from_dict(cls, input_dict: dict) -> typing.Type[Processable]:
        temp_id = input_dict.pop('__id', -1)
        for kwarg_key in input_dict:
            init_kwarg = _child_values_dict[cls][1].get(kwarg_key)
            if init_kwarg:
                if (hasattr(init_kwarg.annotation, '__args__') and
                        len(init_kwarg.annotation.__args__) > 0 and 
                        issubclass(init_kwarg.annotation.__args__[0], Processable)):
                    input_dict[kwarg_key] = [init_kwarg.annotation.__args__[0].from_dict(inst) for inst in input_dict[kwarg_key]]

        result = cls(**input_dict)
        if temp_id != -1:
            result.__id = temp_id
        return result

    @classmethod
    def from_json(cls, json_str: str) -> typing.Type[Processable]:
        kwargs = json.loads(json_str)
        return cls.from_dict(kwargs)


def __ProcessableEncoder(obj: typing.Type[Processable]):
    result = {'__id': obj._Processable__id}
    for attribute in obj._required_attributes:
        value = getattr(obj, attribute)

        if value == _child_values_dict[type(obj)][1][attribute].default:
            continue

        if isinstance(value, enum.Enum):
            value = value.value

        result[attribute] = value

    return result
