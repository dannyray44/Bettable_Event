import inspect
import itertools
import typing
import json
from .metadata import BetType

__child_values_dict: typing.Dict[typing.Type['__Processable'], typing.Tuple[itertools.count, typing.Mapping[str, inspect.Parameter]]] = {}

class __Processable:
    _required_attributes: typing.Optional[typing.List[str]] = None
    _nested_list: typing.Optional[typing.Tuple[str, typing.Type['__Processable']]] = None

    def __init__(self) -> None:
        cls: typing.Type[__Processable] = type(self)
        if cls not in __child_values_dict:
            __child_values_dict[cls] = (
                itertools.count(),
                inspect.signature(cls).parameters
                )
        if not hasattr(self, '__id'):
            self.__id = next(__child_values_dict[cls][0])

    def as_dict(self) -> typing.Dict[str, typing.Any]:
        result = {}
        if self._required_attributes:
            for attribute in self._required_attributes:
                default_val = __child_values_dict[type(self)][1].get(attribute).default
                current_val = getattr(self, attribute)
                if current_val != default_val:
                    result[attribute] = current_val

        if self._nested_list:
            current_attr: typing.List[__Processable] = getattr(self, self._nested_list[0], [])
            # TODO: error catching
            result[self._nested_list[0]] = [val.as_dict() for val in current_attr]

        result['__id'] = self.__id
        return result

    def as_json(self, indent: typing.Optional[int] = None) -> str:
        return json.dumps(self.as_dict(), indent= indent)

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> '__Processable':
        kwargs = {}
        if cls._required_attributes:
            for attribute in cls._required_attributes:
                if attribute in data:
                    kwargs[attribute] = data[attribute]

        if cls._nested_list:
            kwargs[cls._nested_list[0]] = [cls._nested_list[1].from_dict(val) for val in data[cls._nested_list[0]]]

        if not '__id' in data:
            return cls(**kwargs)
    
        result = cls(**kwargs)
        result.__id = data['__id']
        return result

    @classmethod
    def from_json(cls, json_str: str) -> '__Processable':
        return cls.from_dict(json.loads(json_str))

    def update_from_dict(self, data: typing.Dict[str, typing.Any]) -> None:
        if self._nested_list and self._nested_list[0] in data:
            nested_data: typing.List[dict] = data.pop(self._nested_list[0])
            nested_attribute_list: typing.List[__Processable] = getattr(self, self._nested_list[0])
            for nested_dict in nested_data:
                for nested_attribute in nested_attribute_list:
                    if nested_attribute.__id == nested_dict['__id']:
                        nested_attribute.update_from_dict(nested_dict)
                        break
                else:
                    nested_attribute_list.append(self.from_dict(nested_dict))

        for key in data.keys():
            if key == '__id': 
                continue
            setattr(self, key, data[key])

    def update_from_json(self, json_str: str) -> None:
        self.update_from_dict(json.loads(json_str))


class BetValue(__Processable):
    _required_attributes = ['value', 'odds', 'lay', 'volume', 'previous_wager']

    def __init__(self, value: str, odds: float, lay: bool, volume: float = -1.0, previous_wager: float = 0.0, wager: float = 0.0) -> None:
        self.value: str = value
        self.odds: float = odds
        self.lay: bool = lay
        self.volume: float = volume
        self.previous_wager: float = previous_wager
        self.wager: float = wager
        super().__init__()


class Bet(__Processable):
    _required_attributes = ['id']
    _nested_list = 'values', BetValue

    def __init__(self, id: BetType, values: typing.Optional[typing.List[BetValue]] = None) -> None:
        self.id = id
        if values is None:
            values = []
        self.values = values
        super().__init__()

    def as_dict(self) -> typing.Dict[str, typing.Any]:
        result = super().as_dict()
        result['id'] = result['id'].value
        return result
    
    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> '__Processable':
        data['id'] = BetType(data['id'])
        return super().from_dict(data)


class Bookmaker(__Processable):
    _required_attributes = ['commission', 'wager_limit', 'wager_count']
    _nested_list = 'bets', Bet

    def __init__(self, commission: float = 0.0, wager_limit: float = -1.0, wager_count: int = 0, bets: typing.Optional[typing.List[Bet]] = None) -> None:
        self.commission = commission
        self.wager_limit = wager_limit
        self.wager_count = wager_count
        # self.wager_count_limit = -1
        if bets is None:
            bets = []
        self.bets = bets

        super().__init__()


class Event(__Processable):
    _required_attributes = ['total_bet_size', 'profit', 'wager_count']
    _nested_list = 'bookmakers', Bookmaker

    def __init__(self, total_bet_size: float = -1.0, profit: float = -1.0, wager_count: int = -1, bookmakers: typing.Optional[typing.List[Bookmaker]] = None) -> None:
        self.total_bet_size = total_bet_size
        self.profit = profit
        self.wager_count = wager_count
        if bookmakers is None:
            bookmakers = []
        self.bookmakers = bookmakers
        super().__init__()
