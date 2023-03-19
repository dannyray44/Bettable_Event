import inspect
import itertools
import typing
import json
from .metadata import BetType

_child_values_dict: typing.Dict[typing.Type['Processable'], typing.Tuple[itertools.count, typing.Mapping[str, inspect.Parameter]]] = {}

class Processable:
    required_attributes: typing.Optional[typing.List[str]] = None
    nested_list: typing.Optional[typing.Tuple[str, typing.Type['Processable']]] = None

    def __init__(self) -> None:
        cls: typing.Type[Processable] = type(self)
        if cls not in _child_values_dict:
            _child_values_dict[cls] = (
                itertools.count(),
                inspect.signature(cls).parameters
                )
        self.__id = next(_child_values_dict[cls][0])

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        result = {}
        if self.required_attributes:
            for attribute in self.required_attributes:
                result[attribute] = getattr(self, attribute)

        if self.nested_list:
            current_attr = getattr(self, self.nested_list[0], [])
            # TODO: error catching
            result[self.nested_list[0]] = [val.to_dict() for val in current_attr]

        return result

    def to_json(self, indent: typing.Optional[int] = None) -> str:
        return json.dumps(self.to_dict(), indent= indent)
    

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> 'Processable':
        kwargs = {}
        if cls.required_attributes:
            for attribute in cls.required_attributes:
                kwargs[attribute] = data[attribute]

        if cls.nested_list:
            kwargs[cls.nested_list[0]] = [cls.nested_list[1].from_dict(val) for val in data[cls.nested_list[0]]]

        return cls(**kwargs)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Processable':
        return cls.from_json(json.loads(json_str))


class BetValue(Processable):
    required_attributes = ['value', 'odds', 'lay', 'volume', 'previous_wager']

    def __init__(self, value: str, odds: float, lay: bool, volume: float = -1.0, previous_wager: float = 0.0) -> None:
        self.value: str = value
        self.odds: float = odds
        self.lay: bool = lay
        self.volume: float = volume
        self.previous_wager: float = previous_wager
        self.wager: float = 0.0
        super().__init__()


class Bet(Processable):
    required_attributes = ['id']
    nested_list = 'values', BetValue

    def __init__(self, id: BetType, values: typing.Optional[typing.List[BetValue]] = None) -> None:
        self.id = id
        if values is None:
            values = []
        self.values = values
        super().__init__()

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        result = super().to_dict()
        result['id'] = result['id'].value
        return result


class Bookmaker(Processable):
    required_attributes = ['commission', 'wager_limit', 'wager_count']
    nested_list = 'bets', Bet

    def __init__(self, commission: float = 0.0, wager_limit: float = -1.0, wager_count: int = 0, bets: typing.Optional[typing.List[Bet]] = None) -> None:
        self.commission = commission
        self.wager_limit = wager_limit
        self.wager_count = wager_count
        # self.wager_count_limit = -1
        if bets is None:
            bets = []
        self.bets = bets

        super().__init__()


class Event(Processable):
    required_attributes = ['total_bet_size', 'profit', 'wager_count']
    nested_list = 'bookmakers', Bookmaker

    def __init__(self, total_bet_size: float = -1.0, profit: float = -1.0, wager_count: int = -1, bookmakers: typing.Optional[typing.List[Bookmaker]] = None) -> None:
        self.total_bet_size = total_bet_size
        self.profit = profit
        self.wager_count = wager_count
        if bookmakers is None:
            bookmakers = []
        self.bookmakers = bookmakers
        super().__init__()


