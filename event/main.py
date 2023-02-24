# -*- coding: utf-8 -*-
import itertools
import typing
from metadata import BET_TYPE_TABLE

class BetValue:
    __ID_ITTERATOR = itertools.count()

    def __init__(self, value: str, odds: float, lay: bool, volume: float = -1.0, previous_wager: float = 0.0) -> None:
        self.value: str = value
        self.odds: float = odds
        self.lay: bool = lay
        self.volume: float = volume
        self.prevous_wager: float = previous_wager

        self.__id = next(BetValue.__ID_ITTERATOR)

    def _as_minimal_dict(self) -> typing.Dict[str, typing.Union[str, float, bool]]:
        """Return BetValue as a dict that only contians calculation information"""
        return {key: self.__getattribute__(key) for key in ['value', 'odds', 'lay', 'volume', 'prevous_wager', '_BetValue__id']}

class BetType:
    __ID_ITTERATOR = itertools.count()

    def __init__(self, id: typing.Literal[1, 2, 4, 5, 8, 10, 12, 16, 21, 23, 24, 25, 27, 29, 38, 40, 43], values: typing.List[str] = None) -> None:
        self.id = id
        if values is None:
            self.values = []

        self.__instance_id = next(BetType.__ID_ITTERATOR)

class Bookmaker:
    __ID_ITTERATOR = itertools.count()

    def __init__(self, commission: float = 0.0, wager_limit: float = -1.0, bets: typing.List[BetType] = None) -> None:
        self.commission = commission
        self.wager_limit = wager_limit
        if bets is None:
            bets = []
        self.bets = bets

        self.__instance_id = next(Bookmaker.__ID_ITTERATOR)

class Event:
    def __init__(self, bookmakers: typing.List[Bookmaker]) -> None:
        if bookmakers is None:
            bookmakers = []
        self.bookmakers = bookmakers

val = BetValue('str', 2.3, False)

print(val._as_minimal_dict())