from __future__ import annotations

import enum
import inspect
import itertools
import json
import typing

JsonDumpTypes = typing.Union[dict, list, str, int, float, bool]

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
        return json.dumps(self, default=_ProcessableEncoder)
    
    def _update_child_from_dict(self, input_dict: dict) -> None:
        for key, value in input_dict.items():
            self._update_attribute_from_json_var(key, value)

    def _update_child_list_from_list(self, child_list: typing.List[typing.Type[Processable]], input_list: typing.List[dict]) -> None:
        for item in input_list:
            if not '__id' in item:
                raise KeyError('In order to update a list of subclasses from ')

    def _update_attribute_from_json_var(self, attribute_name: str, new_value: JsonDumpTypes) -> None:
        attribute = getattr(self, attribute_name, None)

        if issubclass(type(attribute), Processable):
            if isinstance(new_value, dict):
                attribute._update_child_from_dict(new_value)
            elif isinstance(new_value, list) and all(isinstance(item, dict) for item in new_value):
                for item in new_value:
                    if not '__id' in item:
                        attribute.append(item)
                        continue
                    if item['__id'] == attribute.__id:
                        attribute._update_child_from_dict(item)
            else:
                raise TypeError('Child of Processable: %s must be updated from Dict or List[Dict] not %s', type(attribute), new_value)


        elif isinstance(attribute, list):
            if not isinstance(new_value, list):
                raise TypeError('Attribute %s is type:List and must be updated from list, not %s', attribute, new_value)
            for sub_attribute in attribute:
                if issubclass(type(sub_attribute), Processable) and :
                    sub_attribute._update_attribute_from_json_var()         ###TODO rethink, maybe @static?

        else:

    
    def update_self_from_json(self, json_str: str) -> None:
        json_dict = json.loads(json_str)
        self._update_child_from_dict(json_dict)

    @classmethod
    def _from_dict(cls, input_dict: dict) -> typing.Type[Processable]:
        temp_id = input_dict.pop('__id', -1)
        result = cls(**input_dict)
        if temp_id != -1:
            result.__id = temp_id
        return result

    @classmethod
    def from_json(cls, json_str: str) -> typing.Type[Processable]:
        kwargs = json.loads(json_str)
        return cls._from_dict(kwargs)


def _ProcessableEncoder(obj: typing.Type[Processable]):
    result = {'__id': obj._Processable__id}
    for attribute in obj._required_attributes:
        value = getattr(obj, attribute)

        if value == _child_values_dict[type(obj)][1][attribute].default:
            continue

        if isinstance(value, enum.Enum):
            value = value.value

        result[attribute] = value

    return result
