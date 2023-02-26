# -*- coding: utf-8 -*-
import inspect
import itertools
import typing
from metadata import BetTypeID
from processable import Processable

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

    def _as_transportable_dict(self) -> typing.Dict[str, typing.Union[str, float, bool]]:
        """Return BetValue as a dict that only contains information relevant for calculation"""
        result: typing.Dict[str, typing.Union[str, float, bool]] = {}
        for key in ['value', 'odds', 'lay', 'volume', 'previous_wager']:
            value = self.__getattribute__(key)
            if value != __betvalue_signiture_parameters[key].default:
                result[key] = value

        result['id'] = self._BetValue__id
        return result

    @classmethod
    def from_transportable_dict(cls, transportable_dict: typing.Dict[str, typing.Union[str, float, bool]]) -> 'Bookmaker':
        return cls(**transportable_dict)


class BetType(Processable):
    required_attributes = ['id', 'values']

    def __init__(self, id: typing.Union[int, BetTypeID], values: typing.List[BetValue] = None) -> None:
        if isinstance(id, int):
            id = BetTypeID(id)
        self.id = id

        if values is None:
            values = []
        self.values = values
        super().__init__()

    def _as_transportable_dict(self) -> typing.Dict[str, typing.Union[str, float, bool]]:
        """Return BetType as a dict that only contains information relevant for calculation"""
        result: dict = {'id': self.id.value, '_BetType__id': self.__id}
        result['values'] = [value._as_transportable_dict() for value in self.values]
        return result

    @classmethod
    def from_transportable_dict(cls, transportable_dict: dict) -> 'Bookmaker':
        transportable_dict['values']: typing.List[BetValue] = [BetValue.from_transportable_dict(transportable) for transportable in transportable_dict['values']]
        return cls(**transportable_dict)


class Bookmaker(Processable):
    required_attributes = ['commission', 'wager_limit', 'wager_count', 'bets']

    def __init__(self, commission: float = 0.0, wager_limit: float = -1.0, bets: typing.List[BetType] = None, wager_count: int = 0) -> None:
        self.commission = commission
        self.wager_limit = wager_limit
        self.wager_count = wager_count
        # self.wager_count_limit = -1
        if bets is None:
            bets = []
        self.bets = bets

        super().__init__()

    def _as_transportable_dict(self) -> dict:
        """Return Bookmaker as a dict that only contains information relevant for calculation"""
        result: dict = {}
        for key in ['commision', 'wager_limit']:
            value = self.__getattribute__(key)
            if value != __bookmaker_signiture_parameters[key].default:
                result[key] = value

        result['bets'] = [bet._as_transportable_dict() for bet in self.bets]
        result['id'] = self._Bookmaker__id
        return result

    @classmethod
    def from_transportable_dict(cls, transportable_dict: dict) -> 'Bookmaker':
        transportable_dict['bets']: typing.List[BetType] = [BetType.from_transportable_dict(transportable) for transportable in transportable_dict['bets']]
        return cls(**transportable_dict)


class Event(Processable):
    required_attributes = ['bookmakers', 'total_bet_size', 'profit', 'wager_count']

    def __init__(self, bookmakers: typing.List[Bookmaker] = None, total_bet_size: float = -1.0, profit: float = -1.0, wager_count: int = -1) -> None:
        if bookmakers is None:
            bookmakers = []
        self.bookmakers = bookmakers
        self.total_bet_size = total_bet_size
        self.profit = profit
        self.wager_count = wager_count
        super().__init__()

    def _as_transportable_dict(self) -> typing.Dict[str, typing.Union[str, float, bool]]:
        """Return Event as a dict that only contains information relevant for calculation"""
        result: dict = {}
        for key in ['total_bet_size', 'profit', 'wager_count']:
            value = self.__getattribute__(key)
            if value != __event_signiture_parameters[key].default:
                result[key] = value
        result['bookmakers'] = [bookmaker._as_transportable_dict() for bookmaker in self.bookmakers]
        return result

    @classmethod
    def from_transportable_dict(cls, transportable_dict: dict) -> 'Event':
        transportable_dict['bookmakers']: typing.List[Bookmaker] = [BetType.from_transportable_dict(transportable) for transportable in transportable_dict['bookmakers']]
        return cls(**transportable_dict)


__betvalue_signiture_parameters =   inspect.signature(BetValue  ).parameters
__bookmaker_signiture_parameters =  inspect.signature(Bookmaker ).parameters
__event_signiture_parameters =      inspect.signature(Event     ).parameters

val = BetValue('home', 2.3, False)

ev = Event(bookmakers=[
    Bookmaker(
        wager_limit=135.50,
        bets=[
            BetType(
                1,
                values=[BetValue('home', 2.3, False), BetValue('away', 2.3, False)])
        ])
])

print(ev.to_reduced_dict())

print()
